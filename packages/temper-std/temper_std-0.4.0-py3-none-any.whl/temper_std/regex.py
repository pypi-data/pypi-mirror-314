from abc import ABCMeta as ABCMeta20
from builtins import str as str21, bool as bool22, int as int25, isinstance as isinstance32, len as len15, list as list18, tuple as tuple19
from typing import Callable as Callable23, Sequence as Sequence24, TypeVar as TypeVar26, Generic as Generic27, Union as Union28, Any as Any30, MutableSequence as MutableSequence31, ClassVar as ClassVar35
from types import MappingProxyType as MappingProxyType29
from temper_core import cast_by_type as cast_by_type33, Label as Label34, Pair as Pair0, map_constructor as map_constructor1, list_join as list_join7, generic_eq as generic_eq8, list_get as list_get10, string_from_code_point as string_from_code_point11, string_get as string_get13, string_next as string_next14, int_to_string as int_to_string16, str_cat as str_cat17
from temper_core.regex import regex_compile_formatted as regex_compile_formatted2, regex_compiled_found as regex_compiled_found3, regex_compiled_find as regex_compiled_find4, regex_compiled_replace as regex_compiled_replace5, regex_compiled_split as regex_compiled_split6, regex_formatter_push_capture_name as regex_formatter_push_capture_name9, regex_formatter_push_code_to as regex_formatter_push_code_to12
pair_2759 = Pair0
map_constructor_2760 = map_constructor1
regex_compile_formatted_2761 = regex_compile_formatted2
regex_compiled_found_2762 = regex_compiled_found3
regex_compiled_find_2763 = regex_compiled_find4
regex_compiled_replace_2764 = regex_compiled_replace5
regex_compiled_split_2765 = regex_compiled_split6
list_join_2766 = list_join7
generic_eq_2767 = generic_eq8
regex_formatter_push_capture_name_2769 = regex_formatter_push_capture_name9
list_get_2770 = list_get10
string_from_code_point_2771 = string_from_code_point11
regex_formatter_push_code_to_2772 = regex_formatter_push_code_to12
string_get_2774 = string_get13
string_next_2775 = string_next14
len_2776 = len15
int_to_string_2778 = int_to_string16
str_cat_2779 = str_cat17
list_2780 = list18
tuple_2781 = tuple19
class RegexNode(metaclass = ABCMeta20):
  def compiled(this_42) -> 'Regex':
    return Regex(this_42)
  def found(this_43, text_176: 'str21') -> 'bool22':
    return this_43.compiled().found(text_176)
  def find(this_44, text_179: 'str21') -> 'Match':
    return this_44.compiled().find(text_179)
  def replace(this_45, text_182: 'str21', format_183: 'Callable23[[Match], str21]') -> 'str21':
    return this_45.compiled().replace(text_182, format_183)
  def split(this_46, text_186: 'str21') -> 'Sequence24[str21]':
    return this_46.compiled().split(text_186)
class Capture(RegexNode):
  name_188: 'str21'
  item_189: 'RegexNode'
  __slots__ = ('name_188', 'item_189')
  def __init__(this_91, name_191: 'str21', item_192: 'RegexNode') -> None:
    this_91.name_188 = name_191
    this_91.item_189 = item_192
  @property
  def name(this_479) -> 'str21':
    return this_479.name_188
  @property
  def item(this_482) -> 'RegexNode':
    return this_482.item_189
class CodePart(RegexNode, metaclass = ABCMeta20):
  pass
class CodePoints(CodePart):
  value_193: 'str21'
  __slots__ = ('value_193',)
  def __init__(this_93, value_195: 'str21') -> None:
    this_93.value_193 = value_195
  @property
  def value(this_461) -> 'str21':
    return this_461.value_193
class Special(RegexNode, metaclass = ABCMeta20):
  pass
class SpecialSet(CodePart, Special, metaclass = ABCMeta20):
  pass
class CodeRange(CodePart):
  min_203: 'int25'
  max_204: 'int25'
  __slots__ = ('min_203', 'max_204')
  def __init__(this_109, min_206: 'int25', max_207: 'int25') -> None:
    this_109.min_203 = min_206
    this_109.max_204 = max_207
  @property
  def min(this_485) -> 'int25':
    return this_485.min_203
  @property
  def max(this_488) -> 'int25':
    return this_488.max_204
ITEM_54 = TypeVar26('ITEM_54', bound = RegexNode, covariant = True)
class ItemizedRegex(Generic27[ITEM_54], RegexNode, metaclass = ABCMeta20):
  pass
class CodeSet(ItemizedRegex[CodePart]):
  items_210: 'Sequence24[CodePart]'
  negated_211: 'bool22'
  __slots__ = ('items_210', 'negated_211')
  def __init__(this_113, items_213: 'Sequence24[CodePart]', negated_562: 'Union28[bool22, None]' = None) -> None:
    _negated_562: 'Union28[bool22, None]' = negated_562
    negated_214: 'bool22'
    if _negated_562 is None:
      negated_214 = False
    else:
      negated_214 = _negated_562
    this_113.items_210 = items_213
    this_113.negated_211 = negated_214
  @property
  def items(this_491) -> 'Sequence24[CodePart]':
    return this_491.items_210
  @property
  def negated(this_494) -> 'bool22':
    return this_494.negated_211
class Or(ItemizedRegex[RegexNode]):
  items_215: 'Sequence24[RegexNode]'
  __slots__ = ('items_215',)
  def __init__(this_116, items_217: 'Sequence24[RegexNode]') -> None:
    this_116.items_215 = items_217
  @property
  def items(this_464) -> 'Sequence24[RegexNode]':
    return this_464.items_215
class Repeat(RegexNode):
  item_218: 'RegexNode'
  min_219: 'int25'
  max_220: 'Union28[int25, None]'
  reluctant_221: 'bool22'
  __slots__ = ('item_218', 'min_219', 'max_220', 'reluctant_221')
  def __init__(this_119, item_223: 'RegexNode', min_224: 'int25', max_225: 'Union28[int25, None]', reluctant_564: 'Union28[bool22, None]' = None) -> None:
    _reluctant_564: 'Union28[bool22, None]' = reluctant_564
    reluctant_226: 'bool22'
    if _reluctant_564 is None:
      reluctant_226 = False
    else:
      reluctant_226 = _reluctant_564
    this_119.item_218 = item_223
    this_119.min_219 = min_224
    this_119.max_220 = max_225
    this_119.reluctant_221 = reluctant_226
  @property
  def item(this_497) -> 'RegexNode':
    return this_497.item_218
  @property
  def min(this_500) -> 'int25':
    return this_500.min_219
  @property
  def max(this_503) -> 'Union28[int25, None]':
    return this_503.max_220
  @property
  def reluctant(this_506) -> 'bool22':
    return this_506.reluctant_221
class Sequence(ItemizedRegex[RegexNode]):
  items_235: 'Sequence24[RegexNode]'
  __slots__ = ('items_235',)
  def __init__(this_125, items_237: 'Sequence24[RegexNode]') -> None:
    this_125.items_235 = items_237
  @property
  def items(this_509) -> 'Sequence24[RegexNode]':
    return this_509.items_235
class Match:
  full_238: 'Group'
  groups_239: 'MappingProxyType29[str21, Group]'
  __slots__ = ('full_238', 'groups_239')
  def __init__(this_128, full_241: 'Group', groups_242: 'MappingProxyType29[str21, Group]') -> None:
    this_128.full_238 = full_241
    this_128.groups_239 = groups_242
  @property
  def full(this_455) -> 'Group':
    return this_455.full_238
  @property
  def groups(this_458) -> 'MappingProxyType29[str21, Group]':
    return this_458.groups_239
class Group:
  name_243: 'str21'
  value_244: 'str21'
  begin_245: 'int25'
  end_246: 'int25'
  __slots__ = ('name_243', 'value_244', 'begin_245', 'end_246')
  def __init__(this_131, name_248: 'str21', value_249: 'str21', begin_250: 'int25', end_251: 'int25') -> None:
    this_131.name_243 = name_248
    this_131.value_244 = value_249
    this_131.begin_245 = begin_250
    this_131.end_246 = end_251
  @property
  def name(this_443) -> 'str21':
    return this_443.name_243
  @property
  def value(this_446) -> 'str21':
    return this_446.value_244
  @property
  def begin(this_449) -> 'int25':
    return this_449.begin_245
  @property
  def end(this_452) -> 'int25':
    return this_452.end_246
class RegexRefs_56:
  code_points_252: 'CodePoints'
  group_253: 'Group'
  match_254: 'Match'
  or_object_255: 'Or'
  __slots__ = ('code_points_252', 'group_253', 'match_254', 'or_object_255')
  def __init__(this_133, code_points_554: 'Union28[CodePoints, None]' = None, group_556: 'Union28[Group, None]' = None, match_558: 'Union28[Match, None]' = None, or_object_560: 'Union28[Or, None]' = None) -> None:
    _code_points_554: 'Union28[CodePoints, None]' = code_points_554
    _group_556: 'Union28[Group, None]' = group_556
    _match_558: 'Union28[Match, None]' = match_558
    _or_object_560: 'Union28[Or, None]' = or_object_560
    t_1676: 'CodePoints'
    t_1679: 'Group'
    t_1683: 'MappingProxyType29[str21, Group]'
    t_1684: 'Match'
    t_1687: 'Or'
    code_points_257: 'CodePoints'
    if _code_points_554 is None:
      t_1676 = CodePoints('')
      code_points_257 = t_1676
    else:
      code_points_257 = _code_points_554
    group_258: 'Group'
    if _group_556 is None:
      t_1679 = Group('', '', 0, 0)
      group_258 = t_1679
    else:
      group_258 = _group_556
    match_259: 'Match'
    if _match_558 is None:
      t_1683 = map_constructor_2760((pair_2759('', group_258),))
      t_1684 = Match(group_258, t_1683)
      match_259 = t_1684
    else:
      match_259 = _match_558
    or_object_260: 'Or'
    if _or_object_560 is None:
      t_1687 = Or(())
      or_object_260 = t_1687
    else:
      or_object_260 = _or_object_560
    this_133.code_points_252 = code_points_257
    this_133.group_253 = group_258
    this_133.match_254 = match_259
    this_133.or_object_255 = or_object_260
  @property
  def code_points(this_467) -> 'CodePoints':
    return this_467.code_points_252
  @property
  def group(this_470) -> 'Group':
    return this_470.group_253
  @property
  def match_(this_473) -> 'Match':
    return this_473.match_254
  @property
  def or_object(this_476) -> 'Or':
    return this_476.or_object_255
class Regex:
  data_261: 'RegexNode'
  compiled_279: 'Any30'
  __slots__ = ('data_261', 'compiled_279')
  def __init__(this_57, data_263: 'RegexNode') -> None:
    this_57.data_261 = data_263
    t_1527: 'str21' = this_57.format_304()
    t_1528: 'Any30' = regex_compile_formatted_2761(this_57, t_1527)
    this_57.compiled_279 = t_1528
  def found(this_58, text_266: 'str21') -> 'bool22':
    return regex_compiled_found_2762(this_58, this_58.compiled_279, text_266)
  def find(this_59, text_269: 'str21', begin_566: 'Union28[int25, None]' = None) -> 'Match':
    _begin_566: 'Union28[int25, None]' = begin_566
    begin_270: 'int25'
    if _begin_566 is None:
      begin_270 = 0
    else:
      begin_270 = _begin_566
    return regex_compiled_find_2763(this_59, this_59.compiled_279, text_269, begin_270, regex_refs_168)
  def replace(this_60, text_273: 'str21', format_274: 'Callable23[[Match], str21]') -> 'str21':
    return regex_compiled_replace_2764(this_60, this_60.compiled_279, text_273, format_274, regex_refs_168)
  def split(this_61, text_277: 'str21') -> 'Sequence24[str21]':
    return regex_compiled_split_2765(this_61, this_61.compiled_279, text_277, regex_refs_168)
  def format_304(this_67) -> 'str21':
    return RegexFormatter_68().format(this_67.data_261)
  @property
  def data(this_549) -> 'RegexNode':
    return this_549.data_261
class RegexFormatter_68:
  out_306: 'MutableSequence31[str21]'
  __slots__ = ('out_306',)
  def format(this_69, regex_308: 'RegexNode') -> 'str21':
    this_69.push_regex_311(regex_308)
    def fn_1637(x_310: 'str21') -> 'str21':
      return x_310
    return list_join_2766(this_69.out_306, '', fn_1637)
  def push_regex_311(this_70, regex_312: 'RegexNode') -> 'None':
    t_989: 'Capture'
    t_996: 'CodePoints'
    t_1003: 'CodeRange'
    t_1010: 'CodeSet'
    t_1017: 'Or'
    t_1024: 'Repeat'
    t_1031: 'Sequence'
    if isinstance32(regex_312, Capture):
      t_989 = cast_by_type33(regex_312, Capture)
      this_70.push_capture_314(t_989)
    elif isinstance32(regex_312, CodePoints):
      t_996 = cast_by_type33(regex_312, CodePoints)
      this_70.push_code_points_332(t_996, False)
    elif isinstance32(regex_312, CodeRange):
      t_1003 = cast_by_type33(regex_312, CodeRange)
      this_70.push_code_range_338(t_1003)
    elif isinstance32(regex_312, CodeSet):
      t_1010 = cast_by_type33(regex_312, CodeSet)
      this_70.push_code_set_344(t_1010)
    elif isinstance32(regex_312, Or):
      t_1017 = cast_by_type33(regex_312, Or)
      this_70.push_or_356(t_1017)
    elif isinstance32(regex_312, Repeat):
      t_1024 = cast_by_type33(regex_312, Repeat)
      this_70.push_repeat_360(t_1024)
    elif isinstance32(regex_312, Sequence):
      t_1031 = cast_by_type33(regex_312, Sequence)
      this_70.push_sequence_365(t_1031)
    elif generic_eq_2767(regex_312, begin):
      this_70.out_306.append('^')
    elif generic_eq_2767(regex_312, dot):
      this_70.out_306.append('.')
    elif generic_eq_2767(regex_312, end):
      this_70.out_306.append('$')
    elif generic_eq_2767(regex_312, word_boundary):
      this_70.out_306.append('\\b')
    elif generic_eq_2767(regex_312, digit):
      this_70.out_306.append('\\d')
    elif generic_eq_2767(regex_312, space):
      this_70.out_306.append('\\s')
    elif generic_eq_2767(regex_312, word):
      this_70.out_306.append('\\w')
  def push_capture_314(this_71, capture_315: 'Capture') -> 'None':
    this_71.out_306.append('(')
    t_981: 'MutableSequence31[str21]' = this_71.out_306
    t_1609: 'str21' = capture_315.name
    regex_formatter_push_capture_name_2769(this_71, t_981, t_1609)
    t_1611: 'RegexNode' = capture_315.item
    this_71.push_regex_311(t_1611)
    this_71.out_306.append(')')
  def push_code_321(this_73, code_322: 'int25', inside_code_set_323: 'bool22') -> 'None':
    t_970: 'bool22'
    t_971: 'bool22'
    t_972: 'str21'
    t_974: 'str21'
    t_975: 'bool22'
    t_976: 'bool22'
    t_977: 'bool22'
    t_978: 'bool22'
    t_979: 'str21'
    with Label34() as fn_324:
      special_escape_325: 'str21'
      if code_322 == Codes_85.carriage_return:
        special_escape_325 = 'r'
      elif code_322 == Codes_85.newline:
        special_escape_325 = 'n'
      elif code_322 == Codes_85.tab:
        special_escape_325 = 't'
      else:
        special_escape_325 = ''
      if special_escape_325 != '':
        this_73.out_306.append('\\')
        this_73.out_306.append(special_escape_325)
        fn_324.break_()
      if code_322 <= 127:
        escape_need_326: 'int25'
        escape_need_326 = list_get_2770(escape_needs_169, code_322)
        if escape_need_326 == 2:
          t_971 = True
        else:
          if inside_code_set_323:
            t_970 = code_322 == Codes_85.dash
          else:
            t_970 = False
          t_971 = t_970
        if t_971:
          this_73.out_306.append('\\')
          t_972 = string_from_code_point_2771(code_322)
          this_73.out_306.append(t_972)
          fn_324.break_()
        elif escape_need_326 == 0:
          t_974 = string_from_code_point_2771(code_322)
          this_73.out_306.append(t_974)
          fn_324.break_()
      if code_322 >= Codes_85.supplemental_min:
        t_978 = True
      else:
        if code_322 > Codes_85.high_control_max:
          if Codes_85.surrogate_min <= code_322:
            t_975 = code_322 <= Codes_85.surrogate_max
          else:
            t_975 = False
          if t_975:
            t_976 = True
          else:
            t_976 = code_322 == Codes_85.uint16_max
          t_977 = not t_976
        else:
          t_977 = False
        t_978 = t_977
      if t_978:
        t_979 = string_from_code_point_2771(code_322)
        this_73.out_306.append(t_979)
      else:
        regex_formatter_push_code_to_2772(this_73, this_73.out_306, code_322, inside_code_set_323)
  def push_code_points_332(this_75, code_points_333: 'CodePoints', inside_code_set_334: 'bool22') -> 'None':
    t_1600: 'int25'
    t_966: 'int25'
    value_336: 'str21' = code_points_333.value
    index_337: 'int25' = 0
    while True:
      if not len15(value_336) > index_337:
        break
      t_966 = string_get_2774(value_336, index_337)
      this_75.push_code_321(t_966, inside_code_set_334)
      t_1600 = string_next_2775(value_336, index_337)
      index_337 = t_1600
  def push_code_range_338(this_76, code_range_339: 'CodeRange') -> 'None':
    this_76.out_306.append('[')
    this_76.push_code_range_unwrapped_341(code_range_339)
    this_76.out_306.append(']')
  def push_code_range_unwrapped_341(this_77, code_range_342: 'CodeRange') -> 'None':
    t_1590: 'int25' = code_range_342.min
    this_77.push_code_321(t_1590, True)
    this_77.out_306.append('-')
    t_1592: 'int25' = code_range_342.max
    this_77.push_code_321(t_1592, True)
  def push_code_set_344(this_78, code_set_345: 'CodeSet') -> 'None':
    t_1585: 'int25'
    t_947: 'CodeSet'
    t_953: 'CodePart'
    adjusted_347: 'RegexNode' = this_78.adjust_code_set_349(code_set_345, regex_refs_168)
    if isinstance32(adjusted_347, CodeSet):
      t_947 = cast_by_type33(adjusted_347, CodeSet)
      this_78.out_306.append('[')
      if t_947.negated:
        this_78.out_306.append('^')
      i_348: 'int25' = 0
      while True:
        t_1585 = len_2776(t_947.items)
        if not i_348 < t_1585:
          break
        t_953 = list_get_2770(t_947.items, i_348)
        this_78.push_code_set_item_353(t_953)
        i_348 = i_348 + 1
      this_78.out_306.append(']')
    else:
      this_78.push_regex_311(adjusted_347)
  def adjust_code_set_349(this_79, code_set_350: 'CodeSet', regex_refs_351: 'RegexRefs_56') -> 'RegexNode':
    return code_set_350
  def push_code_set_item_353(this_80, code_part_354: 'CodePart') -> 'None':
    t_925: 'CodePoints'
    t_932: 'CodeRange'
    t_939: 'SpecialSet'
    if isinstance32(code_part_354, CodePoints):
      t_925 = cast_by_type33(code_part_354, CodePoints)
      this_80.push_code_points_332(t_925, True)
    elif isinstance32(code_part_354, CodeRange):
      t_932 = cast_by_type33(code_part_354, CodeRange)
      this_80.push_code_range_unwrapped_341(t_932)
    elif isinstance32(code_part_354, SpecialSet):
      t_939 = cast_by_type33(code_part_354, SpecialSet)
      this_80.push_regex_311(t_939)
  def push_or_356(this_81, or_357: 'Or') -> 'None':
    t_1565: 'int25'
    t_914: 'RegexNode'
    t_919: 'RegexNode'
    if not (not or_357.items):
      this_81.out_306.append('(?:')
      t_914 = list_get_2770(or_357.items, 0)
      this_81.push_regex_311(t_914)
      i_359: 'int25' = 1
      while True:
        t_1565 = len_2776(or_357.items)
        if not i_359 < t_1565:
          break
        this_81.out_306.append('|')
        t_919 = list_get_2770(or_357.items, i_359)
        this_81.push_regex_311(t_919)
        i_359 = i_359 + 1
      this_81.out_306.append(')')
  def push_repeat_360(this_82, repeat_361: 'Repeat') -> 'None':
    t_1556: 'str21'
    t_1557: 'str21'
    t_904: 'bool22'
    t_905: 'bool22'
    t_906: 'bool22'
    this_82.out_306.append('(?:')
    t_1553: 'RegexNode' = repeat_361.item
    this_82.push_regex_311(t_1553)
    this_82.out_306.append(')')
    min_363: 'int25' = repeat_361.min
    max_364: 'Union28[int25, None]'
    max_364 = repeat_361.max
    if min_363 == 0:
      t_904 = max_364 == 1
    else:
      t_904 = False
    if t_904:
      this_82.out_306.append('?')
    else:
      if min_363 == 0:
        t_905 = max_364 is None
      else:
        t_905 = False
      if t_905:
        this_82.out_306.append('*')
      else:
        if min_363 == 1:
          t_906 = max_364 is None
        else:
          t_906 = False
        if t_906:
          this_82.out_306.append('+')
        else:
          t_1556 = int_to_string_2778(min_363)
          this_82.out_306.append(str_cat_2779('{', t_1556))
          if min_363 != max_364:
            this_82.out_306.append(',')
            if not max_364 is None:
              t_1557 = int_to_string_2778(max_364)
              this_82.out_306.append(t_1557)
          this_82.out_306.append('}')
    if repeat_361.reluctant:
      this_82.out_306.append('?')
  def push_sequence_365(this_83, sequence_366: 'Sequence') -> 'None':
    t_1549: 'int25'
    t_898: 'RegexNode'
    i_368: 'int25' = 0
    while True:
      t_1549 = len_2776(sequence_366.items)
      if not i_368 < t_1549:
        break
      t_898 = list_get_2770(sequence_366.items, i_368)
      this_83.push_regex_311(t_898)
      i_368 = i_368 + 1
  def max_code(this_84, code_part_370: 'CodePart') -> 'Union28[int25, None]':
    return_163: 'Union28[int25, None]'
    t_1538: 'int25'
    t_1542: 'Union28[int25, None]'
    t_875: 'CodePoints'
    t_881: 'int25'
    t_890: 'CodeRange'
    if isinstance32(code_part_370, CodePoints):
      t_875 = cast_by_type33(code_part_370, CodePoints)
      value_372: 'str21' = t_875.value
      if not value_372:
        return_163 = None
      else:
        max_373: 'int25' = 0
        index_374: 'int25' = 0
        while True:
          if not len15(value_372) > index_374:
            break
          t_881 = string_get_2774(value_372, index_374)
          next_375: 'int25' = t_881
          if next_375 > max_373:
            max_373 = next_375
          t_1538 = string_next_2775(value_372, index_374)
          index_374 = t_1538
        return_163 = max_373
    elif isinstance32(code_part_370, CodeRange):
      t_890 = cast_by_type33(code_part_370, CodeRange)
      t_1542 = t_890.max
      return_163 = t_1542
    elif generic_eq_2767(code_part_370, digit):
      return_163 = Codes_85.digit9
    elif generic_eq_2767(code_part_370, space):
      return_163 = Codes_85.space
    elif generic_eq_2767(code_part_370, word):
      return_163 = Codes_85.lower_z
    else:
      return_163 = None
    return return_163
  def __init__(this_146) -> None:
    t_1530: 'MutableSequence31[str21]' = list_2780()
    this_146.out_306 = t_1530
class Codes_85:
  ampersand: ClassVar35['int25']
  backslash: ClassVar35['int25']
  caret: ClassVar35['int25']
  carriage_return: ClassVar35['int25']
  curly_left: ClassVar35['int25']
  curly_right: ClassVar35['int25']
  dash: ClassVar35['int25']
  dot: ClassVar35['int25']
  high_control_min: ClassVar35['int25']
  high_control_max: ClassVar35['int25']
  digit0: ClassVar35['int25']
  digit9: ClassVar35['int25']
  lower_a: ClassVar35['int25']
  lower_z: ClassVar35['int25']
  newline: ClassVar35['int25']
  peso: ClassVar35['int25']
  pipe: ClassVar35['int25']
  plus: ClassVar35['int25']
  question: ClassVar35['int25']
  round_left: ClassVar35['int25']
  round_right: ClassVar35['int25']
  slash: ClassVar35['int25']
  square_left: ClassVar35['int25']
  square_right: ClassVar35['int25']
  star: ClassVar35['int25']
  tab: ClassVar35['int25']
  tilde: ClassVar35['int25']
  upper_a: ClassVar35['int25']
  upper_z: ClassVar35['int25']
  space: ClassVar35['int25']
  surrogate_min: ClassVar35['int25']
  surrogate_max: ClassVar35['int25']
  supplemental_min: ClassVar35['int25']
  uint16_max: ClassVar35['int25']
  underscore: ClassVar35['int25']
  __slots__ = ()
  def __init__(this_165) -> None:
    pass
Codes_85.ampersand = 38
Codes_85.backslash = 92
Codes_85.caret = 94
Codes_85.carriage_return = 13
Codes_85.curly_left = 123
Codes_85.curly_right = 125
Codes_85.dash = 45
Codes_85.dot = 46
Codes_85.high_control_min = 127
Codes_85.high_control_max = 159
Codes_85.digit0 = 48
Codes_85.digit9 = 57
Codes_85.lower_a = 97
Codes_85.lower_z = 122
Codes_85.newline = 10
Codes_85.peso = 36
Codes_85.pipe = 124
Codes_85.plus = 43
Codes_85.question = 63
Codes_85.round_left = 40
Codes_85.round_right = 41
Codes_85.slash = 47
Codes_85.square_left = 91
Codes_85.square_right = 93
Codes_85.star = 42
Codes_85.tab = 9
Codes_85.tilde = 42
Codes_85.upper_a = 65
Codes_85.upper_z = 90
Codes_85.space = 32
Codes_85.surrogate_min = 55296
Codes_85.surrogate_max = 57343
Codes_85.supplemental_min = 65536
Codes_85.uint16_max = 65535
Codes_85.underscore = 95
regex_refs_168: 'RegexRefs_56' = RegexRefs_56()
class Begin_47(Special):
  __slots__ = ()
  def __init__(this_95) -> None:
    pass
begin: 'Special' = Begin_47()
class Dot_48(Special):
  __slots__ = ()
  def __init__(this_97) -> None:
    pass
dot: 'Special' = Dot_48()
class End_49(Special):
  __slots__ = ()
  def __init__(this_99) -> None:
    pass
end: 'Special' = End_49()
class WordBoundary_50(Special):
  __slots__ = ()
  def __init__(this_101) -> None:
    pass
word_boundary: 'Special' = WordBoundary_50()
class Digit_51(SpecialSet):
  __slots__ = ()
  def __init__(this_103) -> None:
    pass
digit: 'SpecialSet' = Digit_51()
class Space_52(SpecialSet):
  __slots__ = ()
  def __init__(this_105) -> None:
    pass
space: 'SpecialSet' = Space_52()
class Word_53(SpecialSet):
  __slots__ = ()
  def __init__(this_107) -> None:
    pass
word: 'SpecialSet' = Word_53()
def build_escape_needs_167() -> 'Sequence24[int25]':
  t_1044: 'bool22'
  t_1045: 'bool22'
  t_1046: 'bool22'
  t_1047: 'bool22'
  t_1048: 'bool22'
  t_1049: 'bool22'
  t_1050: 'bool22'
  t_1051: 'bool22'
  t_1052: 'bool22'
  t_1053: 'bool22'
  t_1054: 'bool22'
  t_1055: 'bool22'
  t_1056: 'bool22'
  t_1057: 'bool22'
  t_1058: 'bool22'
  t_1059: 'bool22'
  t_1060: 'bool22'
  t_1061: 'bool22'
  t_1062: 'bool22'
  t_1063: 'bool22'
  t_1064: 'bool22'
  t_1065: 'bool22'
  t_1066: 'bool22'
  t_1067: 'bool22'
  t_1068: 'int25'
  escape_needs_378: 'MutableSequence31[int25]' = list_2780()
  code_379: 'int25' = 0
  while code_379 < 127:
    if code_379 == Codes_85.dash:
      t_1051 = True
    else:
      if code_379 == Codes_85.space:
        t_1050 = True
      else:
        if code_379 == Codes_85.underscore:
          t_1049 = True
        else:
          if Codes_85.digit0 <= code_379:
            t_1044 = code_379 <= Codes_85.digit9
          else:
            t_1044 = False
          if t_1044:
            t_1048 = True
          else:
            if Codes_85.upper_a <= code_379:
              t_1045 = code_379 <= Codes_85.upper_z
            else:
              t_1045 = False
            if t_1045:
              t_1047 = True
            else:
              if Codes_85.lower_a <= code_379:
                t_1046 = code_379 <= Codes_85.lower_z
              else:
                t_1046 = False
              t_1047 = t_1046
            t_1048 = t_1047
          t_1049 = t_1048
        t_1050 = t_1049
      t_1051 = t_1050
    if t_1051:
      t_1068 = 0
    else:
      if code_379 == Codes_85.ampersand:
        t_1067 = True
      else:
        if code_379 == Codes_85.backslash:
          t_1066 = True
        else:
          if code_379 == Codes_85.caret:
            t_1065 = True
          else:
            if code_379 == Codes_85.curly_left:
              t_1064 = True
            else:
              if code_379 == Codes_85.curly_right:
                t_1063 = True
              else:
                if code_379 == Codes_85.dot:
                  t_1062 = True
                else:
                  if code_379 == Codes_85.peso:
                    t_1061 = True
                  else:
                    if code_379 == Codes_85.pipe:
                      t_1060 = True
                    else:
                      if code_379 == Codes_85.plus:
                        t_1059 = True
                      else:
                        if code_379 == Codes_85.question:
                          t_1058 = True
                        else:
                          if code_379 == Codes_85.round_left:
                            t_1057 = True
                          else:
                            if code_379 == Codes_85.round_right:
                              t_1056 = True
                            else:
                              if code_379 == Codes_85.slash:
                                t_1055 = True
                              else:
                                if code_379 == Codes_85.square_left:
                                  t_1054 = True
                                else:
                                  if code_379 == Codes_85.square_right:
                                    t_1053 = True
                                  else:
                                    if code_379 == Codes_85.star:
                                      t_1052 = True
                                    else:
                                      t_1052 = code_379 == Codes_85.tilde
                                    t_1053 = t_1052
                                  t_1054 = t_1053
                                t_1055 = t_1054
                              t_1056 = t_1055
                            t_1057 = t_1056
                          t_1058 = t_1057
                        t_1059 = t_1058
                      t_1060 = t_1059
                    t_1061 = t_1060
                  t_1062 = t_1061
                t_1063 = t_1062
              t_1064 = t_1063
            t_1065 = t_1064
          t_1066 = t_1065
        t_1067 = t_1066
      if t_1067:
        t_1068 = 2
      else:
        t_1068 = 1
    escape_needs_378.append(t_1068)
    code_379 = code_379 + 1
  return tuple_2781(escape_needs_378)
escape_needs_169: 'Sequence24[int25]' = build_escape_needs_167()
def entire(item_227: 'RegexNode') -> 'RegexNode':
  return Sequence((begin, item_227, end))
def one_or_more(item_229: 'RegexNode', reluctant_568: 'Union28[bool22, None]' = None) -> 'Repeat':
  _reluctant_568: 'Union28[bool22, None]' = reluctant_568
  reluctant_230: 'bool22'
  if _reluctant_568 is None:
    reluctant_230 = False
  else:
    reluctant_230 = _reluctant_568
  return Repeat(item_229, 1, None, reluctant_230)
def optional(item_232: 'RegexNode', reluctant_570: 'Union28[bool22, None]' = None) -> 'Repeat':
  _reluctant_570: 'Union28[bool22, None]' = reluctant_570
  reluctant_233: 'bool22'
  if _reluctant_570 is None:
    reluctant_233 = False
  else:
    reluctant_233 = _reluctant_570
  return Repeat(item_232, 0, 1, reluctant_233)
