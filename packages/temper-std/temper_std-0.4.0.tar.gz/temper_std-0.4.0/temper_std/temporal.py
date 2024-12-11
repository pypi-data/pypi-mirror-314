from temper_std.json import JsonProducer as JsonProducer_35, JsonSyntaxTree as JsonSyntaxTree_37, InterchangeContext as InterchangeContext_34, JsonString as JsonString_36
from datetime import date as date64
from builtins import str as str21, int as int25, bool as bool22, list as list18, len as len15
from temper_core import cast_by_type as cast_by_type33, date_to_string as date_to_string62, int_to_string as int_to_string16, string_get as string_get13, string_next as string_next14, string_count_between as string_count_between63
from typing import Sequence as Sequence24
from temper_std.json import JsonAdapter
date_to_string_2830 = date_to_string62
int_to_string_2831 = int_to_string16
len_2832 = len15
string_get_2833 = string_get13
string_next_2835 = string_next14
string_count_between_2836 = string_count_between63
class DateJsonAdapter_106(JsonAdapter[date64]):
  __slots__ = ()
  def encode_to_json(this_116, x_112: 'date64', p_113: 'JsonProducer_35') -> 'None':
    encode_to_json_87(x_112, p_113)
  def decode_from_json(this_117, t_114: 'JsonSyntaxTree_37', ic_115: 'InterchangeContext_34') -> 'date64':
    return decode_from_json_90(t_114, ic_115)
  def __init__(this_118) -> None:
    pass
# Type nym`std//temporal.temper.md`.Date connected to datetime.date
def encode_to_json_87(this_16: 'date64', p_88: 'JsonProducer_35') -> 'None':
  t_340: 'str21' = date_to_string_2830(this_16)
  p_88.string_value(t_340)
def decode_from_json_90(t_91: 'JsonSyntaxTree_37', ic_92: 'InterchangeContext_34') -> 'date64':
  t_196: 'JsonString_36'
  t_196 = cast_by_type33(t_91, JsonString_36)
  t_338: 'str21' = t_196.content
  return from_iso_string_59(t_338)
def json_adapter_120() -> 'JsonAdapter[date64]':
  return DateJsonAdapter_106()
days_in_month_30: 'Sequence24[int25]' = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
def is_leap_year_28(year_38: 'int25') -> 'bool22':
  return_17: 'bool22'
  t_267: 'int25'
  if year_38 % 4 == 0:
    if year_38 % 100 != 0:
      return_17 = True
    else:
      t_267 = year_38 % 400
      return_17 = t_267 == 0
  else:
    return_17 = False
  return return_17
def pad_to_29(min_width_40: 'int25', num_41: 'int25', sb_42: 'list18[str21]') -> 'None':
  "If the decimal representation of \\|num\\| is longer than [minWidth],\nthen appends that representation.\nOtherwise any sign for [num] followed by enough zeroes to bring the\nwhole length up to [minWidth].\n\n```temper\n// When the width is greater than the decimal's length,\n// we pad to that width.\n\"0123\" == do {\n  let sb = new StringBuilder();\n  padTo(4, 123, sb);\n  sb.toString()\n}\n\n// When the width is the same or lesser, we just use the string form.\n\"123\" == do {\n  let sb = new StringBuilder();\n  padTo(2, 123, sb);\n  sb.toString()\n}\n\n// The sign is always on the left.\n\"-01\" == do {\n  let sb = new StringBuilder();\n  padTo(3, -1, sb);\n  sb.toString()\n}\n```"
  t_379: 'int25'
  decimal_44: 'str21' = int_to_string_2831(num_41, 10)
  decimal_index_45: 'int25' = 0
  decimal_end_46: 'int25' = len_2832(decimal_44)
  t_261: 'int25'
  t_261 = string_get_2833(decimal_44, decimal_index_45)
  if t_261 == 45:
    sb_42.append('-')
    t_379 = string_next_2835(decimal_44, decimal_index_45)
    decimal_index_45 = t_379
  t_380: 'int25' = string_count_between_2836(decimal_44, decimal_index_45, decimal_end_46)
  n_needed_47: 'int25' = min_width_40 - t_380
  while n_needed_47 > 0:
    sb_42.append('0')
    n_needed_47 = n_needed_47 - 1
  sb_42.append(decimal_44[decimal_index_45 : decimal_end_46])
day_of_week_lookup_table_leapy_32: 'Sequence24[int25]' = (0, 0, 3, 4, 0, 2, 5, 0, 3, 6, 1, 4, 6)
day_of_week_lookup_table_not_leapy_33: 'Sequence24[int25]' = (0, 0, 3, 3, 6, 1, 4, 6, 2, 5, 0, 3, 5)
