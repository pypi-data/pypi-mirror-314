from pydantic import BaseModel
from urllib.request import urlopen
import requests
import xmltodict
import random
from typing import List, Tuple

from .bro_objects import CPTCharacteristics, Envelope, Point
from ..objects.cpt import Cpt, CptReadError
from ..settings import BRO_CPT_DOWNLOAD_URL, BRO_CPT_CHARACTERISTICS_URL
from ..gis.helpers import xy_to_latlon, xy_regularly_spaced, latlon_to_xy
from ..helpers import distance_to_line

BRO_API_REQUEST_LINE_DISTANCE = 1000  # the line length that is used per BRO call if you request data along a polyline


class BROAPI(BaseModel):
    def _get_cpt_metadata_by_bounds(
        self,
        left: float,
        top: float,
        right: float,
        bottom: float,
        exclude_bro_ids: List[str] = [],
        max_num: int = -1,
    ):
        # add BRO_ to the exclude list because it is added to the ID
        # exclude_bro_ids = [f"BRO_{s}" for s in exclude_bro_ids]

        envelope = Envelope(
            lower_corner=Point(lat=left, lon=bottom),
            upper_corner=Point(lat=right, lon=top),
        )

        headers = {
            "accept": "application/xml",
            "Content-Type": "application/json",
        }

        json = {"area": envelope.bro_json}

        response = requests.post(
            BRO_CPT_CHARACTERISTICS_URL, headers=headers, json=json, timeout=10
        )

        available_cpt_objects = []

        # TODO: Check status codes in BRO REST API documentation.
        if response.status_code == 200:
            parsed = xmltodict.parse(
                response.content, attr_prefix="", cdata_key="value"
            )
            rejection_reason = parsed["dispatchCharacteristicsResponse"].get(
                "brocom:rejectionReason"
            )
            if rejection_reason:
                raise ValueError(f"{rejection_reason}")

            nr_of_documents = int(
                parsed["dispatchCharacteristicsResponse"].get("numberOfDocuments")
            )
            if nr_of_documents is None or nr_of_documents == 0:
                raise ValueError(
                    "No available objects have been found in given date + area range. Retry with different parameters."
                )

            if nr_of_documents == 1:
                documents = [
                    parsed["dispatchCharacteristicsResponse"]["dispatchDocument"]
                ]
            else:
                documents = parsed["dispatchCharacteristicsResponse"][
                    "dispatchDocument"
                ]

            for document in documents:
                # TODO: Hard skip, this is likely to happen when it's deregistered. document will have key ["BRO_DO"]["brocom:deregistered"] = "ja"
                # TODO: Add this information to logger
                if "CPT_C" not in document.keys():
                    continue

                bro_id = f"{document['CPT_C']['brocom:broId']}"

                if not bro_id in exclude_bro_ids:
                    available_cpt_objects.append(CPTCharacteristics(document["CPT_C"]))

            if max_num != -1 and len(available_cpt_objects) > max_num:
                available_cpt_objects = random.choices(available_cpt_objects, k=max_num)

            return available_cpt_objects

        response.raise_for_status()

    def get_cpt_from_bro_id(self, bro_id):
        URL = f"{BRO_CPT_DOWNLOAD_URL}/{bro_id}"
        try:
            s = urlopen(URL).read()
            cpt = Cpt.from_string(s, suffix=".xml")
            # add BRO_ as a prefix
            # cpt.name = f"BRO_{cpt.name}"
            return s, cpt
        except Exception as e:
            raise CptReadError(
                f"Error reading cpt file from url '{URL}', got error '{e}' "
            )

    def get_cpts_by_bounds_latlon(
        self,
        left: float,
        right: float,
        top: float,
        bottom: float,
        exclude_bro_ids: List[str] = [],
        max_num: int = -1,
    ):
        cpt_characteristics = self._get_cpt_metadata_by_bounds(
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            exclude_bro_ids=exclude_bro_ids,
            max_num=max_num,
        )

        return self._cpt_metadata_to_cpts(cpt_characteristics)

    def get_cpts_meta_data_by_bounds_latlon(
        self,
        left: float,
        right: float,
        top: float,
        bottom: float,
        exclude_bro_ids: List[str] = [],
        max_num: int = -1,
    ):
        cpt_characteristics = self._get_cpt_metadata_by_bounds(
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            exclude_bro_ids=exclude_bro_ids,
            max_num=max_num,
        )

        return cpt_characteristics

    def get_cpts_by_bounds_rd(
        self,
        left: float,
        right: float,
        top: float,
        bottom: float,
        exclude_bro_ids: List[str] = [],
        max_num: int = -1,
    ):
        lat1, lon1 = xy_to_latlon(left, bottom)
        lat2, lon2 = xy_to_latlon(right, top)

        cpt_characteristics = self._get_cpt_metadata_by_bounds(
            left=lat1,
            top=lon2,
            right=lat2,
            bottom=lon1,
            exclude_bro_ids=exclude_bro_ids,
            max_num=max_num,
        )
        return self._cpt_metadata_to_cpts(cpt_characteristics)

    def get_cpts_meta_data_by_bounds_rd(
        self,
        left: float,
        right: float,
        top: float,
        bottom: float,
        exclude_bro_ids: List[str] = [],
        max_num: int = -1,
    ):
        lat1, lon1 = xy_to_latlon(left, bottom)
        lat2, lon2 = xy_to_latlon(right, top)

        cpt_characteristics = self._get_cpt_metadata_by_bounds(
            left=lat1,
            top=lon2,
            right=lat2,
            bottom=lon1,
            exclude_bro_ids=exclude_bro_ids,
            max_num=max_num,
        )

        return cpt_characteristics

    def _cpt_metadata_to_cpts(self, cpt_metadata):
        cpt_strings, cpts = [], []
        for cpt_c in cpt_metadata:
            try:
                cpt_string, cpt = self.get_cpt_from_bro_id(cpt_c.bro_id)
            except CptReadError:
                # no friction
                continue

            cpt_strings.append(cpt_string)
            cpts.append(cpt)

        return cpt_strings, cpts

    def get_cpts_along_line_latlon(
        self,
        points: List[Tuple[float, float]],
        max_distance: float = 10.0,
        exclude_bro_ids: List[str] = [],
    ):
        cpt_characteristics = self.get_cpts_meta_data_along_line_latlon(
            points=points, max_distance=max_distance, exclude_bro_ids=exclude_bro_ids
        )
        return self._cpt_metadata_to_cpts(cpt_characteristics)

    def get_cpts_along_line_xy(
        self,
        points: List[Tuple[float, float]],
        max_distance: float = 10.0,
        exclude_bro_ids: List[str] = [],
    ):
        cpt_characteristics = self.get_cpts_meta_data_along_line_xy(
            points=points, max_distance=max_distance, exclude_bro_ids=exclude_bro_ids
        )
        return self._cpt_metadata_to_cpts(cpt_characteristics)

    def get_cpts_meta_data_along_line_latlon(
        self,
        points: List[Tuple[float, float]],
        max_distance: float = 10.0,
        exclude_bro_ids: List[str] = [],
    ):
        xys = [latlon_to_xy(p[0], p[1]) for p in points]
        return self.get_cpts_meta_data_along_line_xy(
            xys, max_distance=max_distance, exclude_bro_ids=exclude_bro_ids
        )

    def get_cpts_meta_data_along_line_xy(
        self,
        points: List[Tuple[float, float]],
        max_distance: float = 10.0,
        exclude_bro_ids: List[str] = [],
    ):
        cxy = xy_regularly_spaced(points, spacing=5)
        # make a request every 1km
        c_start, c_end = 0, BRO_API_REQUEST_LINE_DISTANCE
        done = False
        cpts_metadatas = []
        while not done:
            pts = [p for p in cxy if c_start <= p[0] and p[0] < c_end]
            done = len(pts) == 0

            if not done:
                xs = [p[1] for p in pts]
                ys = [p[2] for p in pts]
                left = min(xs) - max_distance
                right = max(xs) + max_distance
                top = max(ys) + max_distance
                bottom = min(ys) - max_distance
                exclude_ids = exclude_bro_ids + [c.bro_id for c in cpts_metadatas]
                mds = self.get_cpts_meta_data_by_bounds_rd(
                    left=left,
                    right=right,
                    bottom=bottom,
                    top=top,
                    exclude_bro_ids=exclude_ids,
                )
                if len(mds) > 0:
                    cpts_metadatas += mds

            c_start = c_end
            c_end += BRO_API_REQUEST_LINE_DISTANCE

        # now check the distance to the line and remove those that are too far away
        # final_result = []
        # xys = [(p[1], p[2]) for p in cxy]
        # for md in cpts_metadatas:
        #     x = md.rd_coordinate.x
        #     y = md.rd_coordinate.y
        #     if (
        #         distance_to_line((x, y), xys) <= max_distance
        #     ):  # TODO this does not work for latlon!
        #         final_result.append(md)

        return cpts_metadatas
