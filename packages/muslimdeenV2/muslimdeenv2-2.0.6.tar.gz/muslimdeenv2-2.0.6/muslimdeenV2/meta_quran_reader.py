from muslimdeenV2.quran_reader import QuranReader, QuranSourateData, QuranVersetData
from muslimdeenV2.exception_handle import SurahNotFound, VersetNotFound, FormatValueGet
from typing import Optional, Dict, List, Tuple, TypedDict, Literal, Union
import re


FilterVersets = Literal['position_ds_sourate']


class FilterVersetsDict (TypedDict):
    position_ds_sourate: int


class MetaQuranReader(QuranReader):
    def __init__(self, path_database):
        super().__init__(path_database)
        self.__lower_name_fr: Optional[Dict[str, QuranSourateData]] = None

    @property
    def lower_name_fr(self) -> Dict[str, QuranSourateData]:
        if self.__lower_name_fr is None:
            self.__lower_name_fr = {
                k.lower(): v for k, v in self.sourate_by_name_fr.items()
            }
        return self.__lower_name_fr

    def get_number_range(self, a: int = 1, b: int = 10) -> List[QuranSourateData]:
        data_quran = self.sourate_by_number
        result: List[QuranSourateData] = []
        for k, v in data_quran.items():
            if a <= k <= b:
                result.append(v)
        return result

    def get_name_fr(self, *names: Tuple[str]) -> Tuple[QuranSourateData]:
        names_lower = [name.lower() for name in list(names)]
        data: List[QuranSourateData] = []
        for name in names_lower:
            sourate = self.lower_name_fr.get(name, None)
            if sourate is None:
                raise SurahNotFound(f"Surah not found {name}")
            data.append(sourate)
        return tuple(data)

    def get_number(self, *numbers: Tuple[int]) -> Tuple[QuranSourateData]:
        data: List[QuranSourateData] = []
        for i in numbers:
            surah = self.sourate_by_number.get(i, None)
            if surah is None:
                raise SurahNotFound(f"Position surah not found {i}")
            data.append(surah)
        return tuple(data)

    def get_arabic(self, *args: Tuple[str]) -> Tuple[QuranSourateData]:
        data: List[QuranSourateData] = []
        for name_arabic in args:
            surah = self.sourate_by_name_arabic.get(name_arabic, None)
            if surah is None:
                raise SurahNotFound(f"Surah not found {name_arabic}")
            data.append(surah)
        return tuple(data)

    def get_simple_page(self, page: int) -> List[QuranSourateData]:
        data_pages: List[QuranSourateData] = []
        for sourate in self.quran['sourates']:
            for verset in sourate["versets"]:
                if verset["page"] == page and sourate not in data_pages:
                    data_pages.append(sourate)
        return data_pages

    def get_last_page(self) -> List[QuranSourateData]:
        last_surahs = self.search_by_number(114)
        len_versets = len(last_surahs["versets"])
        last_verset = last_surahs["versets"][len_versets - 1]
        last_pages: List[QuranSourateData] = []
        for sourate in self.quran["sourates"]:
            for verset in sourate["versets"]:
                if verset["page"] == last_verset["page"] and sourate not in last_pages:
                    last_pages.append(sourate)
        return last_pages

    def filter_versets(self, filter_by: str, value: dict, data: QuranSourateData) -> Optional[QuranVersetData]:
        value_filter = value[filter_by]
        for verset in data["versets"]:
            for k, v in verset.items():
                if filter_by == k and value_filter == v:
                    return verset
        return None

    def get_filter(
        self,
        type_filter: Literal["fr", "arabic", "number"],
        value_filter: Union[str, int],
        type_filter_versets: Optional[FilterVersets] = None,
        value_filter_versets: Optional[FilterVersetsDict] = None
    ) -> Union[Tuple[QuranSourateData, Optional[QuranVersetData]], Tuple[None, None]]:
        func_dict = {
            "fr": self.get_name_fr,
            "arabic": self.get_arabic,
            "number": self.get_number
        }
        func_filter = {
            "position_ds_sourate": self.filter_versets
        }

        data: Optional[Tuple[QuranSourateData]
                       ] = func_dict[type_filter](value_filter)
        if data is None:
            raise SurahNotFound("Surah not found")
        if type_filter_versets is not None:
            data_filter: Optional[QuranVersetData] = func_filter[type_filter_versets](
                type_filter_versets, value_filter_versets, data[0]
            )
            if data_filter is None:
                raise VersetNotFound("Type filter versets not found")
            return data[0], data_filter
        return data[0], None

    def get(self, value: str):
        if not self.check_format_get(value):
            raise FormatValueGet("Format value not matched")
        values = value.split(":")
        if len(values) > 1:
            surah, verset = values
            surah = int(surah)
            verset = int(verset)
            data_s, data_v = self.get_filter("number", surah, "position_ds_sourate", {
                "position_ds_sourate": verset
            })
        else:
            values = int(values[0])
            data_s, data_v = self.get_filter("number", values)
        return data_s, data_v

    def check_format_get(self, value: str) -> bool:
        pattern = r'^\d+(?::\d+)?$'
        return bool(re.match(pattern, value))
