from abc import ABCMeta as ABCMeta20, abstractmethod as abstractmethod55
from builtins import str as str21, RuntimeError as RuntimeError54, bool as bool22, int as int25, float as float56, Exception as Exception39, list as list18, isinstance as isinstance32, len as len15, chr as chr58, tuple as tuple19
from typing import Union as Union28, ClassVar as ClassVar35, Sequence as Sequence24, MutableSequence as MutableSequence31, Dict as Dict57, Any as Any30, TypeVar as TypeVar26, Generic as Generic27
from types import MappingProxyType as MappingProxyType29
from temper_core import Label as Label34, cast_by_type as cast_by_type33, require_string_index as require_string_index59, list_get as list_get10, list_for_each as list_for_each40, mapped_for_each as mapped_for_each41, int_to_string as int_to_string16, int_to_float64 as int_to_float6442, float64_to_string as float64_to_string43, float64_to_int as float64_to_int44, string_to_float64 as string_to_float6445, list_get_or as list_get_or46, list_builder_set as list_builder_set47, mapped_has as mapped_has48, map_builder_set as map_builder_set49, mapped_to_map as mapped_to_map50, string_get as string_get13, string_next as string_next14, string_has_at_least as string_has_at_least51, float_lt_eq as float_lt_eq52, float_not_eq as float_not_eq53
from math import nan as nan60, inf as inf61
from temper_std.regex import str_cat_2779, generic_eq_2767
len_2794 = len15
list_get_2795 = list_get10
list_for_each_2796 = list_for_each40
mapped_for_each_2797 = mapped_for_each41
int_to_string_2798 = int_to_string16
int_to_float64_2799 = int_to_float6442
float64_to_string_2800 = float64_to_string43
float64_to_int_2801 = float64_to_int44
string_to_float64_2803 = string_to_float6445
list_2805 = list18
list_get_or_2807 = list_get_or46
list_builder_set_2808 = list_builder_set47
mapped_has_2815 = mapped_has48
map_builder_set_2817 = map_builder_set49
tuple_2818 = tuple19
mapped_to_map_2819 = mapped_to_map50
string_get_2821 = string_get13
string_next_2822 = string_next14
string_has_at_least_2826 = string_has_at_least51
float_lt_eq_2828 = float_lt_eq52
float_not_eq_2829 = float_not_eq53
class InterchangeContext(metaclass = ABCMeta20):
  def get_header(this_71, header_name_327: 'str21') -> 'Union28[str21, None]':
    raise RuntimeError54()
class NullInterchangeContext(InterchangeContext):
  instance: ClassVar35['NullInterchangeContext']
  __slots__ = ()
  def get_header(this_72, header_name_330: 'str21') -> 'Union28[str21, None]':
    return None
  def __init__(this_164) -> None:
    pass
NullInterchangeContext.instance = NullInterchangeContext()
class JsonProducer(metaclass = ABCMeta20):
  @property
  @abstractmethod55
  def interchange_context(self) -> 'InterchangeContext':
    pass
  def start_object(this_73) -> 'None':
    raise RuntimeError54()
  def end_object(this_74) -> 'None':
    raise RuntimeError54()
  def object_key(this_75, key_340: 'str21') -> 'None':
    raise RuntimeError54()
  def start_array(this_76) -> 'None':
    raise RuntimeError54()
  def end_array(this_77) -> 'None':
    raise RuntimeError54()
  def null_value(this_78) -> 'None':
    raise RuntimeError54()
  def boolean_value(this_79, x_349: 'bool22') -> 'None':
    raise RuntimeError54()
  def int_value(this_80, x_352: 'int25') -> 'None':
    raise RuntimeError54()
  def float64_value(this_81, x_355: 'float56') -> 'None':
    raise RuntimeError54()
  def numeric_token_value(this_82, x_358: 'str21') -> 'None':
    'A number that fits the JSON number grammar to allow\ninterchange of numbers that are not easily represntible\nusing numeric types that Temper connects to.'
    raise RuntimeError54()
  def string_value(this_83, x_361: 'str21') -> 'None':
    raise RuntimeError54()
class JsonSyntaxTree(metaclass = ABCMeta20):
  def produce(this_84, p_364: 'JsonProducer') -> 'None':
    raise RuntimeError54()
class JsonObject(JsonSyntaxTree):
  properties_366: 'MappingProxyType29[str21, (Sequence24[JsonSyntaxTree])]'
  __slots__ = ('properties_366',)
  def property_value_or_null(this_85, property_key_368: 'str21') -> 'Union28[JsonSyntaxTree, None]':
    "The JSON value tree associated with the given property key or null\nif there is no such value.\n\nThe properties map contains a list of sub-trees because JSON\nallows duplicate properties.  ECMA-404 \xa76 notes (emphasis added):\n\n> The JSON syntax does not impose any restrictions on the strings\n> used as names, **does not require that name strings be unique**,\n> and does not assign any significance to the ordering of\n> name/value pairs.\n\nWhen widely used JSON parsers need to relate a property key\nto a single value, they tend to prefer the last key/value pair\nfrom a JSON object.  For example:\n\nJS:\n\n    JSON.parse('{\"x\":\"first\",\"x\":\"last\"}').x === 'last'\n\nPython:\n\n    import json\n    json.loads('{\"x\":\"first\",\"x\":\"last\"}')['x'] == 'last'\n\nC#:\n\n   using System.Text.Json;\n\t\tJsonDocument d = JsonDocument.Parse(\n\t\t\t\"\"\"\n\t\t\t{\"x\":\"first\",\"x\":\"last\"}\n\t\t\t\"\"\"\n\t\t);\n\t\td.RootElement.GetProperty(\"x\").GetString() == \"last\""
    return_182: 'Union28[JsonSyntaxTree, None]'
    tree_list_370: 'Sequence24[JsonSyntaxTree]' = this_85.properties_366.get(property_key_368, ())
    last_index_371: 'int25' = len_2794(tree_list_370) - 1
    if last_index_371 >= 0:
      return_182 = list_get_2795(tree_list_370, last_index_371)
    else:
      return_182 = None
    return return_182
  def property_value_or_bubble(this_86, property_key_373: 'str21') -> 'JsonSyntaxTree':
    return_183: 'JsonSyntaxTree'
    t_1755: 'Union28[JsonSyntaxTree, None]'
    t_1755 = this_86.property_value_or_null(property_key_373)
    t_841: 'Union28[JsonSyntaxTree, None]' = t_1755
    if t_841 is None:
      raise RuntimeError54()
    else:
      return_183 = t_841
    return return_183
  def produce(this_87, p_376: 'JsonProducer') -> 'None':
    p_376.start_object()
    def fn_2732(k_378: 'str21', vs_379: 'Sequence24[JsonSyntaxTree]') -> 'None':
      def fn_2728(v_380: 'JsonSyntaxTree') -> 'None':
        p_376.object_key(k_378)
        v_380.produce(p_376)
      list_for_each_2796(vs_379, fn_2728)
    mapped_for_each_2797(this_87.properties_366, fn_2732)
    p_376.end_object()
  def __init__(this_179, properties_382: 'MappingProxyType29[str21, (Sequence24[JsonSyntaxTree])]') -> None:
    this_179.properties_366 = properties_382
  @property
  def properties(this_769) -> 'MappingProxyType29[str21, (Sequence24[JsonSyntaxTree])]':
    return this_769.properties_366
class JsonArray(JsonSyntaxTree):
  elements_383: 'Sequence24[JsonSyntaxTree]'
  __slots__ = ('elements_383',)
  def produce(this_88, p_385: 'JsonProducer') -> 'None':
    p_385.start_array()
    def fn_2717(v_387: 'JsonSyntaxTree') -> 'None':
      v_387.produce(p_385)
    list_for_each_2796(this_88.elements_383, fn_2717)
    p_385.end_array()
  def __init__(this_185, elements_389: 'Sequence24[JsonSyntaxTree]') -> None:
    this_185.elements_383 = elements_389
  @property
  def elements(this_772) -> 'Sequence24[JsonSyntaxTree]':
    return this_772.elements_383
class JsonBoolean(JsonSyntaxTree):
  content_390: 'bool22'
  __slots__ = ('content_390',)
  def produce(this_89, p_392: 'JsonProducer') -> 'None':
    p_392.boolean_value(this_89.content_390)
  def __init__(this_189, content_395: 'bool22') -> None:
    this_189.content_390 = content_395
  @property
  def content(this_775) -> 'bool22':
    return this_775.content_390
class JsonNull(JsonSyntaxTree):
  __slots__ = ()
  def produce(this_90, p_397: 'JsonProducer') -> 'None':
    p_397.null_value()
  def __init__(this_192) -> None:
    pass
class JsonString(JsonSyntaxTree):
  content_400: 'str21'
  __slots__ = ('content_400',)
  def produce(this_91, p_402: 'JsonProducer') -> 'None':
    p_402.string_value(this_91.content_400)
  def __init__(this_195, content_405: 'str21') -> None:
    this_195.content_400 = content_405
  @property
  def content(this_778) -> 'str21':
    return this_778.content_400
class JsonNumeric(JsonSyntaxTree, metaclass = ABCMeta20):
  def as_json_numeric_token(this_92) -> 'str21':
    raise RuntimeError54()
  def as_int(this_93) -> 'int25':
    raise RuntimeError54()
  def as_float64(this_94) -> 'float56':
    raise RuntimeError54()
class JsonInt(JsonNumeric):
  content_412: 'int25'
  __slots__ = ('content_412',)
  def produce(this_95, p_414: 'JsonProducer') -> 'None':
    p_414.int_value(this_95.content_412)
  def as_json_numeric_token(this_96) -> 'str21':
    return int_to_string_2798(this_96.content_412)
  def as_int(this_97) -> 'int25':
    return this_97.content_412
  def as_float64(this_98) -> 'float56':
    return int_to_float64_2799(this_98.content_412)
  def __init__(this_201, content_423: 'int25') -> None:
    this_201.content_412 = content_423
  @property
  def content(this_781) -> 'int25':
    return this_781.content_412
class JsonFloat64(JsonNumeric):
  content_424: 'float56'
  __slots__ = ('content_424',)
  def produce(this_99, p_426: 'JsonProducer') -> 'None':
    p_426.float64_value(this_99.content_424)
  def as_json_numeric_token(this_100) -> 'str21':
    return float64_to_string_2800(this_100.content_424)
  def as_int(this_101) -> 'int25':
    return float64_to_int_2801(this_101.content_424)
  def as_float64(this_102) -> 'float56':
    return this_102.content_424
  def __init__(this_207, content_435: 'float56') -> None:
    this_207.content_424 = content_435
  @property
  def content(this_784) -> 'float56':
    return this_784.content_424
class JsonNumericToken(JsonNumeric):
  content_436: 'str21'
  __slots__ = ('content_436',)
  def produce(this_103, p_438: 'JsonProducer') -> 'None':
    p_438.numeric_token_value(this_103.content_436)
  def as_json_numeric_token(this_104) -> 'str21':
    return this_104.content_436
  def as_int(this_105) -> 'int25':
    return_217: 'int25'
    t_1729: 'int25'
    t_1730: 'float56'
    try:
      t_1729 = int(this_105.content_436)
      return_217 = t_1729
    except Exception39:
      t_1730 = string_to_float64_2803(this_105.content_436)
      return_217 = float64_to_int_2801(t_1730)
    return return_217
  def as_float64(this_106) -> 'float56':
    return string_to_float64_2803(this_106.content_436)
  def __init__(this_213, content_447: 'str21') -> None:
    this_213.content_436 = content_447
  @property
  def content(this_787) -> 'str21':
    return this_787.content_436
class JsonTextProducer(JsonProducer):
  interchange_context_448: 'InterchangeContext'
  buffer_449: 'list18[str21]'
  stack_450: 'MutableSequence31[int25]'
  well_formed_451: 'bool22'
  __slots__ = ('interchange_context_448', 'buffer_449', 'stack_450', 'well_formed_451')
  def __init__(this_107, interchange_context_829: 'Union28[InterchangeContext, None]' = None) -> None:
    _interchange_context_829: 'Union28[InterchangeContext, None]' = interchange_context_829
    interchange_context_453: 'InterchangeContext'
    if _interchange_context_829 is None:
      interchange_context_453 = NullInterchangeContext.instance
    else:
      interchange_context_453 = _interchange_context_829
    this_107.interchange_context_448 = interchange_context_453
    t_2658: 'list18[str21]' = ['']
    this_107.buffer_449 = t_2658
    t_2659: 'MutableSequence31[int25]' = list_2805()
    this_107.stack_450 = t_2659
    this_107.stack_450.append(5)
    this_107.well_formed_451 = True
  def state_455(this_108) -> 'int25':
    t_2653: 'int25' = len_2794(this_108.stack_450)
    return list_get_or_2807(this_108.stack_450, t_2653 - 1, -1)
  def before_value_457(this_109) -> 'None':
    t_2645: 'int25'
    t_2648: 'int25'
    t_2650: 'int25'
    t_1686: 'bool22'
    current_state_459: 'int25' = this_109.state_455()
    if current_state_459 == 3:
      t_2645 = len_2794(this_109.stack_450)
      list_builder_set_2808(this_109.stack_450, t_2645 - 1, 4)
    elif current_state_459 == 4:
      this_109.buffer_449.append(',')
    elif current_state_459 == 1:
      t_2648 = len_2794(this_109.stack_450)
      list_builder_set_2808(this_109.stack_450, t_2648 - 1, 2)
    elif current_state_459 == 5:
      t_2650 = len_2794(this_109.stack_450)
      list_builder_set_2808(this_109.stack_450, t_2650 - 1, 6)
    else:
      if current_state_459 == 6:
        t_1686 = True
      else:
        t_1686 = current_state_459 == 2
      if t_1686:
        this_109.well_formed_451 = False
  def start_object(this_110) -> 'None':
    this_110.before_value_457()
    this_110.buffer_449.append('{')
    this_110.stack_450.append(0)
  def end_object(this_111) -> 'None':
    t_1674: 'bool22'
    this_111.buffer_449.append('}')
    current_state_464: 'int25' = this_111.state_455()
    if 0 == current_state_464:
      t_1674 = True
    else:
      t_1674 = 2 == current_state_464
    if t_1674:
      this_111.stack_450.pop()
    else:
      this_111.well_formed_451 = False
  def object_key(this_112, key_466: 'str21') -> 'None':
    t_2635: 'int25'
    current_state_468: 'int25' = this_112.state_455()
    if not current_state_468 == 0:
      if current_state_468 == 2:
        this_112.buffer_449.append(',')
      else:
        this_112.well_formed_451 = False
    encode_json_string_303(key_466, this_112.buffer_449)
    this_112.buffer_449.append(':')
    if current_state_468 >= 0:
      t_2635 = len_2794(this_112.stack_450)
      list_builder_set_2808(this_112.stack_450, t_2635 - 1, 1)
  def start_array(this_113) -> 'None':
    this_113.before_value_457()
    this_113.buffer_449.append('[')
    this_113.stack_450.append(3)
  def end_array(this_114) -> 'None':
    t_1662: 'bool22'
    this_114.buffer_449.append(']')
    current_state_473: 'int25' = this_114.state_455()
    if 3 == current_state_473:
      t_1662 = True
    else:
      t_1662 = 4 == current_state_473
    if t_1662:
      this_114.stack_450.pop()
    else:
      this_114.well_formed_451 = False
  def null_value(this_115) -> 'None':
    this_115.before_value_457()
    this_115.buffer_449.append('null')
  def boolean_value(this_116, x_477: 'bool22') -> 'None':
    t_1658: 'str21'
    this_116.before_value_457()
    if x_477:
      t_1658 = 'true'
    else:
      t_1658 = 'false'
    this_116.buffer_449.append(t_1658)
  def int_value(this_117, x_480: 'int25') -> 'None':
    this_117.before_value_457()
    t_2616: 'str21' = int_to_string_2798(x_480)
    this_117.buffer_449.append(t_2616)
  def float64_value(this_118, x_483: 'float56') -> 'None':
    this_118.before_value_457()
    t_2612: 'str21' = float64_to_string_2800(x_483)
    this_118.buffer_449.append(t_2612)
  def numeric_token_value(this_119, x_486: 'str21') -> 'None':
    this_119.before_value_457()
    this_119.buffer_449.append(x_486)
  def string_value(this_120, x_489: 'str21') -> 'None':
    this_120.before_value_457()
    encode_json_string_303(x_489, this_120.buffer_449)
  def to_json_string(this_121) -> 'str21':
    return_233: 'str21'
    t_2602: 'int25'
    t_1649: 'bool22'
    t_1650: 'bool22'
    if this_121.well_formed_451:
      if len_2794(this_121.stack_450) == 1:
        t_2602 = this_121.state_455()
        t_1649 = t_2602 == 6
      else:
        t_1649 = False
      t_1650 = t_1649
    else:
      t_1650 = False
    if t_1650:
      return_233 = ''.join(this_121.buffer_449)
    else:
      raise RuntimeError54()
    return return_233
  @property
  def interchange_context(this_797) -> 'InterchangeContext':
    return this_797.interchange_context_448
class JsonParseErrorReceiver(metaclass = ABCMeta20):
  def explain_json_error(this_122, explanation_509: 'str21') -> 'None':
    raise RuntimeError54()
class JsonSyntaxTreeProducer(JsonProducer, JsonParseErrorReceiver):
  stack_511: 'MutableSequence31[(MutableSequence31[JsonSyntaxTree])]'
  error_512: 'Union28[str21, None]'
  interchange_context_237: 'InterchangeContext'
  json_error_238: 'Union28[str21, None]'
  __slots__ = ('stack_511', 'error_512', 'interchange_context_237', 'json_error_238')
  @property
  def interchange_context(this_123) -> 'InterchangeContext':
    return NullInterchangeContext.instance
  def __init__(this_124) -> None:
    t_2595: 'MutableSequence31[(MutableSequence31[JsonSyntaxTree])]' = list_2805()
    this_124.stack_511 = t_2595
    t_2596: 'MutableSequence31[JsonSyntaxTree]' = list_2805()
    this_124.stack_511.append(t_2596)
    this_124.error_512 = None
  def store_value_517(this_125, v_518: 'JsonSyntaxTree') -> 'None':
    t_2593: 'int25'
    t_1640: 'MutableSequence31[JsonSyntaxTree]'
    if not (not this_125.stack_511):
      t_2593 = len_2794(this_125.stack_511)
      t_1640 = list_get_2795(this_125.stack_511, t_2593 - 1)
      t_1640.append(v_518)
  def start_object(this_126) -> 'None':
    t_2590: 'MutableSequence31[JsonSyntaxTree]' = list_2805()
    this_126.stack_511.append(t_2590)
  def end_object(this_127) -> 'None':
    t_2579: 'Union28[(Dict57[str21, (MutableSequence31[JsonSyntaxTree])]), None]'
    t_2587: 'JsonObject'
    t_1615: 'JsonSyntaxTree'
    t_1619: 'JsonString'
    t_1623: 'JsonSyntaxTree'
    t_1626: 'Dict57[str21, (MutableSequence31[JsonSyntaxTree])]'
    t_1629: 'Sequence24[JsonSyntaxTree]'
    t_1631: 'MutableSequence31[JsonSyntaxTree]'
    with Label34() as fn_523:
      if not this_127.stack_511:
        fn_523.break_()
      ls_524: 'MutableSequence31[JsonSyntaxTree]'
      ls_524 = this_127.stack_511.pop()
      m_525: 'Dict57[str21, (Sequence24[JsonSyntaxTree])]' = {}
      multis_526: 'Union28[(Dict57[str21, (MutableSequence31[JsonSyntaxTree])]), None]' = None
      i_527: 'int25' = 0
      n_528: 'int25' = len_2794(ls_524) & -2
      while i_527 < n_528:
        postfix_return_34: 'int25' = i_527
        i_527 = i_527 + 1
        t_1615 = list_get_2795(ls_524, postfix_return_34)
        key_tree_529: 'JsonSyntaxTree' = t_1615
        if not isinstance32(key_tree_529, JsonString):
          break
        t_1619 = cast_by_type33(key_tree_529, JsonString)
        key_530: 'str21' = t_1619.content
        postfix_return_35: 'int25' = i_527
        i_527 = i_527 + 1
        t_1623 = list_get_2795(ls_524, postfix_return_35)
        value_531: 'JsonSyntaxTree' = t_1623
        if mapped_has_2815(m_525, key_530):
          if multis_526 is None:
            t_2579 = {}
            multis_526 = t_2579
          if multis_526 is None:
            raise RuntimeError54()
          else:
            t_1626 = multis_526
          mb_532: 'Dict57[str21, (MutableSequence31[JsonSyntaxTree])]' = t_1626
          if not mapped_has_2815(mb_532, key_530):
            t_1629 = m_525[key_530]
            map_builder_set_2817(mb_532, key_530, list_2805(t_1629))
          t_1631 = mb_532[key_530]
          t_1631.append(value_531)
        else:
          map_builder_set_2817(m_525, key_530, (value_531,))
      multis_533: 'Union28[(Dict57[str21, (MutableSequence31[JsonSyntaxTree])]), None]' = multis_526
      if not multis_533 is None:
        def fn_2569(k_534: 'str21', vs_535: 'MutableSequence31[JsonSyntaxTree]') -> 'None':
          t_2566: 'Sequence24[JsonSyntaxTree]' = tuple_2818(vs_535)
          map_builder_set_2817(m_525, k_534, t_2566)
        mapped_for_each_2797(multis_533, fn_2569)
      t_2587 = JsonObject(mapped_to_map_2819(m_525))
      this_127.store_value_517(t_2587)
  def object_key(this_128, key_537: 'str21') -> 'None':
    t_2563: 'JsonString' = JsonString(key_537)
    this_128.store_value_517(t_2563)
  def start_array(this_129) -> 'None':
    t_2561: 'MutableSequence31[JsonSyntaxTree]' = list_2805()
    this_129.stack_511.append(t_2561)
  def end_array(this_130) -> 'None':
    t_2558: 'JsonArray'
    with Label34() as fn_542:
      if not this_130.stack_511:
        fn_542.break_()
      ls_543: 'MutableSequence31[JsonSyntaxTree]'
      ls_543 = this_130.stack_511.pop()
      t_2558 = JsonArray(tuple_2818(ls_543))
      this_130.store_value_517(t_2558)
  def null_value(this_131) -> 'None':
    t_2552: 'JsonNull' = JsonNull()
    this_131.store_value_517(t_2552)
  def boolean_value(this_132, x_547: 'bool22') -> 'None':
    t_2549: 'JsonBoolean' = JsonBoolean(x_547)
    this_132.store_value_517(t_2549)
  def int_value(this_133, x_550: 'int25') -> 'None':
    t_2546: 'JsonInt' = JsonInt(x_550)
    this_133.store_value_517(t_2546)
  def float64_value(this_134, x_553: 'float56') -> 'None':
    t_2543: 'JsonFloat64' = JsonFloat64(x_553)
    this_134.store_value_517(t_2543)
  def numeric_token_value(this_135, x_556: 'str21') -> 'None':
    t_2540: 'JsonNumericToken' = JsonNumericToken(x_556)
    this_135.store_value_517(t_2540)
  def string_value(this_136, x_559: 'str21') -> 'None':
    t_2537: 'JsonString' = JsonString(x_559)
    this_136.store_value_517(t_2537)
  def to_json_syntax_tree(this_137) -> 'JsonSyntaxTree':
    t_1590: 'bool22'
    if len_2794(this_137.stack_511) != 1:
      t_1590 = True
    else:
      t_1590 = not this_137.error_512 is None
    if t_1590:
      raise RuntimeError54()
    ls_563: 'MutableSequence31[JsonSyntaxTree]'
    ls_563 = list_get_2795(this_137.stack_511, 0)
    if len_2794(ls_563) != 1:
      raise RuntimeError54()
    return list_get_2795(ls_563, 0)
  @property
  def json_error(this_138) -> 'Union28[str21, None]':
    return this_138.error_512
  def explain_json_error(this_139, error_567: 'str21') -> 'None':
    this_139.error_512 = error_567
def parse_json_value_308(source_text_587: 'str21', i_588: 'int25', out_589: 'JsonProducer') -> 'int25':
  return_260: 'int25'
  t_2327: 'int25'
  t_1351: 'int25'
  t_1355: 'bool22'
  with Label34() as fn_590:
    t_2327 = skip_json_spaces_307(source_text_587, i_588)
    i_588 = t_2327
    if not len15(source_text_587) > i_588:
      expected_token_error_305(source_text_587, i_588, out_589, 'JSON value')
      return_260 = -1
      fn_590.break_()
    t_1351 = string_get_2821(source_text_587, i_588)
    if t_1351 == 123:
      return_260 = parse_json_object_309(source_text_587, i_588, out_589)
    elif t_1351 == 91:
      return_260 = parse_json_array_310(source_text_587, i_588, out_589)
    elif t_1351 == 34:
      return_260 = parse_json_string_311(source_text_587, i_588, out_589)
    else:
      if t_1351 == 116:
        t_1355 = True
      else:
        t_1355 = t_1351 == 102
      if t_1355:
        return_260 = parse_json_boolean_313(source_text_587, i_588, out_589)
      elif t_1351 == 110:
        return_260 = parse_json_null_314(source_text_587, i_588, out_589)
      else:
        return_260 = parse_json_number_316(source_text_587, i_588, out_589)
  return return_260
T_140 = TypeVar26('T_140', bound = Any30, covariant = True)
class JsonAdapter(Generic27[T_140], metaclass = ABCMeta20):
  def encode_to_json(this_141, x_671: 'T_140', p_672: 'JsonProducer') -> 'None':
    raise RuntimeError54()
  def decode_from_json(this_142, t_675: 'JsonSyntaxTree', ic_676: 'InterchangeContext') -> 'T_140':
    raise RuntimeError54()
class BooleanJsonAdapter_143(JsonAdapter[bool22]):
  __slots__ = ()
  def encode_to_json(this_144, x_679: 'bool22', p_680: 'JsonProducer') -> 'None':
    p_680.boolean_value(x_679)
  def decode_from_json(this_145, t_683: 'JsonSyntaxTree', ic_684: 'InterchangeContext') -> 'bool22':
    t_1329: 'JsonBoolean'
    t_1329 = cast_by_type33(t_683, JsonBoolean)
    return t_1329.content
  def __init__(this_272) -> None:
    pass
class Float64JsonAdapter_146(JsonAdapter[float56]):
  __slots__ = ()
  def encode_to_json(this_147, x_689: 'float56', p_690: 'JsonProducer') -> 'None':
    p_690.float64_value(x_689)
  def decode_from_json(this_148, t_693: 'JsonSyntaxTree', ic_694: 'InterchangeContext') -> 'float56':
    t_1325: 'JsonFloat64'
    t_1325 = cast_by_type33(t_693, JsonFloat64)
    return t_1325.content
  def __init__(this_277) -> None:
    pass
class IntJsonAdapter_149(JsonAdapter[int25]):
  __slots__ = ()
  def encode_to_json(this_150, x_699: 'int25', p_700: 'JsonProducer') -> 'None':
    p_700.int_value(x_699)
  def decode_from_json(this_151, t_703: 'JsonSyntaxTree', ic_704: 'InterchangeContext') -> 'int25':
    t_1321: 'JsonInt'
    t_1321 = cast_by_type33(t_703, JsonInt)
    return t_1321.content
  def __init__(this_282) -> None:
    pass
class StringJsonAdapter_152(JsonAdapter[str21]):
  __slots__ = ()
  def encode_to_json(this_153, x_709: 'str21', p_710: 'JsonProducer') -> 'None':
    p_710.string_value(x_709)
  def decode_from_json(this_154, t_713: 'JsonSyntaxTree', ic_714: 'InterchangeContext') -> 'str21':
    t_1317: 'JsonString'
    t_1317 = cast_by_type33(t_713, JsonString)
    return t_1317.content
  def __init__(this_287) -> None:
    pass
T_156 = TypeVar26('T_156', bound = Any30)
class ListJsonAdapter_155(JsonAdapter[(Sequence24[T_156])]):
  adapter_for_t_718: 'JsonAdapter[T_156]'
  __slots__ = ('adapter_for_t_718',)
  def encode_to_json(this_157, x_720: 'Sequence24[T_156]', p_721: 'JsonProducer') -> 'None':
    p_721.start_array()
    def fn_2277(el_723: 'T_156') -> 'None':
      this_157.adapter_for_t_718.encode_to_json(el_723, p_721)
    list_for_each_2796(x_720, fn_2277)
    p_721.end_array()
  def decode_from_json(this_158, t_725: 'JsonSyntaxTree', ic_726: 'InterchangeContext') -> 'Sequence24[T_156]':
    t_1310: 'JsonSyntaxTree'
    t_1311: 'T_156'
    b_728: 'MutableSequence31[T_156]' = list_2805()
    t_1306: 'JsonArray'
    t_1306 = cast_by_type33(t_725, JsonArray)
    elements_729: 'Sequence24[JsonSyntaxTree]' = t_1306.elements
    n_730: 'int25' = len_2794(elements_729)
    i_731: 'int25' = 0
    while i_731 < n_730:
      t_1310 = list_get_2795(elements_729, i_731)
      el_732: 'JsonSyntaxTree' = t_1310
      i_731 = i_731 + 1
      t_1311 = this_158.adapter_for_t_718.decode_from_json(el_732, ic_726)
      b_728.append(t_1311)
    return tuple_2818(b_728)
  def __init__(this_292, adapter_for_t_734: 'JsonAdapter[T_156]') -> None:
    this_292.adapter_for_t_718 = adapter_for_t_734
T_160 = TypeVar26('T_160', bound = Any30)
class OrNullJsonAdapter(JsonAdapter[(Union28[T_160, None])]):
  adapter_for_t_737: 'JsonAdapter[T_160]'
  __slots__ = ('adapter_for_t_737',)
  def encode_to_json(this_161, x_739: 'Union28[T_160, None]', p_740: 'JsonProducer') -> 'None':
    if x_739 is None:
      p_740.null_value()
    else:
      x_836: 'T_160' = x_739
      this_161.adapter_for_t_737.encode_to_json(x_836, p_740)
  def decode_from_json(this_162, t_743: 'JsonSyntaxTree', ic_744: 'InterchangeContext') -> 'Union28[T_160, None]':
    return_302: 'Union28[T_160, None]'
    if isinstance32(t_743, JsonNull):
      return_302 = None
    else:
      return_302 = this_162.adapter_for_t_737.decode_from_json(t_743, ic_744)
    return return_302
  def __init__(this_298, adapter_for_t_747: 'JsonAdapter[T_160]') -> None:
    this_298.adapter_for_t_737 = adapter_for_t_747
hex_digits_324: 'Sequence24[str21]' = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')
def encode_hex4_304(cp_501: 'int25', buffer_502: 'list18[str21]') -> 'None':
  b0_504: 'int25' = cp_501 // 4096 & 15
  b1_505: 'int25' = cp_501 // 256 & 15
  b2_506: 'int25' = cp_501 // 16 & 15
  b3_507: 'int25' = cp_501 & 15
  t_1718: 'str21'
  t_1718 = list_get_2795(hex_digits_324, b0_504)
  buffer_502.append(t_1718)
  t_1720: 'str21'
  t_1720 = list_get_2795(hex_digits_324, b1_505)
  buffer_502.append(t_1720)
  t_1722: 'str21'
  t_1722 = list_get_2795(hex_digits_324, b2_506)
  buffer_502.append(t_1722)
  t_1724: 'str21'
  t_1724 = list_get_2795(hex_digits_324, b3_507)
  buffer_502.append(t_1724)
def encode_json_string_303(x_493: 'str21', buffer_494: 'list18[str21]') -> 'None':
  t_1702: 'int25'
  t_1703: 'bool22'
  t_1704: 'bool22'
  t_1705: 'str21'
  t_1706: 'str21'
  buffer_494.append('"')
  i_496: 'int25' = 0
  emitted_497: 'int25' = i_496
  while True:
    if not len15(x_493) > i_496:
      break
    t_1702 = string_get_2821(x_493, i_496)
    cp_498: 'int25' = t_1702
    if cp_498 == 8:
      t_1706 = '\\b'
    elif cp_498 == 9:
      t_1706 = '\\t'
    elif cp_498 == 10:
      t_1706 = '\\n'
    elif cp_498 == 12:
      t_1706 = '\\f'
    elif cp_498 == 13:
      t_1706 = '\\r'
    elif cp_498 == 34:
      t_1706 = '\\"'
    elif cp_498 == 92:
      t_1706 = '\\\\'
    else:
      if cp_498 < 32:
        t_1704 = True
      else:
        if 55296 <= cp_498:
          t_1703 = cp_498 <= 57343
        else:
          t_1703 = False
        t_1704 = t_1703
      if t_1704:
        t_1705 = '\\u'
      else:
        t_1705 = ''
      t_1706 = t_1705
    replacement_499: 'str21' = t_1706
    next_i_500: 'int25' = string_next_2822(x_493, i_496)
    if replacement_499 != '':
      buffer_494.append(x_493[emitted_497 : i_496])
      buffer_494.append(replacement_499)
      if replacement_499 == '\\u':
        encode_hex4_304(cp_498, buffer_494)
      emitted_497 = next_i_500
    i_496 = next_i_500
  buffer_494.append(x_493[emitted_497 : i_496])
  buffer_494.append('"')
def store_json_error_306(out_575: 'JsonProducer', explanation_576: 'str21') -> 'None':
  if isinstance32(out_575, JsonParseErrorReceiver):
    error_receiver_578: 'JsonParseErrorReceiver'
    error_receiver_578 = cast_by_type33(out_575, JsonParseErrorReceiver)
    error_receiver_578.explain_json_error(explanation_576)
def expected_token_error_305(source_text_569: 'str21', i_570: 'int25', out_571: 'JsonProducer', short_explanation_572: 'str21') -> 'None':
  t_2524: 'int25'
  t_2525: 'str21'
  gotten_574: 'str21'
  if len15(source_text_569) > i_570:
    t_2524 = len_2794(source_text_569)
    t_2525 = source_text_569[i_570 : t_2524]
    gotten_574 = str_cat_2779('`', t_2525, '`')
  else:
    gotten_574 = 'end-of-file'
  store_json_error_306(out_571, str_cat_2779('Expected ', short_explanation_572, ', but got ', gotten_574))
def skip_json_spaces_307(source_text_584: 'str21', i_585: 'int25') -> 'int25':
  t_2520: 'int25'
  t_1571: 'int25'
  t_1572: 'bool22'
  t_1573: 'bool22'
  t_1574: 'bool22'
  while True:
    if not len15(source_text_584) > i_585:
      break
    t_1571 = string_get_2821(source_text_584, i_585)
    if t_1571 == 9:
      t_1574 = True
    else:
      if t_1571 == 10:
        t_1573 = True
      else:
        if t_1571 == 13:
          t_1572 = True
        else:
          t_1572 = t_1571 == 32
        t_1573 = t_1572
      t_1574 = t_1573
    if not t_1574:
      break
    t_2520 = string_next_2822(source_text_584, i_585)
    i_585 = t_2520
  return i_585
def decode_hex_unsigned_312(source_text_618: 'str21', start_619: 'int25', limit_620: 'int25') -> 'int25':
  return_264: 'int25'
  t_2517: 'int25'
  t_1564: 'int25'
  t_1565: 'bool22'
  t_1566: 'bool22'
  t_1567: 'bool22'
  t_1568: 'int25'
  with Label34() as fn_621:
    n_622: 'int25' = 0
    i_623: 'int25' = start_619
    while True:
      if not i_623 - limit_620 < 0:
        break
      t_1564 = string_get_2821(source_text_618, i_623)
      cp_624: 'int25' = t_1564
      if 48 <= cp_624:
        t_1565 = cp_624 <= 48
      else:
        t_1565 = False
      if t_1565:
        t_1568 = cp_624 - 48
      else:
        if 65 <= cp_624:
          t_1566 = cp_624 <= 70
        else:
          t_1566 = False
        if t_1566:
          t_1568 = cp_624 - 65 + 10
        else:
          if 97 <= cp_624:
            t_1567 = cp_624 <= 102
          else:
            t_1567 = False
          if t_1567:
            t_1568 = cp_624 - 97 + 10
          else:
            return_264 = -1
            fn_621.break_()
      digit_625: 'int25' = t_1568
      n_622 = n_622 * 16 + digit_625
      t_2517 = string_next_2822(source_text_618, i_623)
      i_623 = t_2517
    return_264 = n_622
  return return_264
def parse_json_string_311(source_text_602: 'str21', i_603: 'int25', out_604: 'JsonProducer') -> 'int25':
  return_263: 'int25'
  t_2476: 'int25'
  t_2481: 'int25'
  t_2486: 'int25'
  t_2488: 'int25'
  t_2489: 'int25'
  t_2490: 'int25'
  t_2491: 'int25'
  t_2492: 'int25'
  t_2510: 'int25'
  t_2512: 'str21'
  t_1519: 'int25'
  t_1520: 'bool22'
  t_1526: 'int25'
  t_1530: 'int25'
  t_1532: 'bool22'
  t_1533: 'bool22'
  t_1541: 'int25'
  t_1542: 'int25'
  t_1544: 'int25'
  t_1546: 'int25'
  t_1547: 'bool22'
  t_1548: 'int25'
  t_1549: 'bool22'
  t_1550: 'bool22'
  t_1554: 'int25'
  t_1555: 'bool22'
  with Label34() as fn_605:
    if not len15(source_text_602) > i_603:
      t_1520 = True
    else:
      t_1519 = string_get_2821(source_text_602, i_603)
      t_1520 = t_1519 != 34
    if t_1520:
      expected_token_error_305(source_text_602, i_603, out_604, '"')
      return_263 = -1
      fn_605.break_()
    t_2476 = string_next_2822(source_text_602, i_603)
    i_603 = t_2476
    sb_606: 'list18[str21]' = ['']
    lead_surrogate_607: 'int25' = -1
    consumed_608: 'int25' = i_603
    while True:
      if not len15(source_text_602) > i_603:
        break
      t_1526 = string_get_2821(source_text_602, i_603)
      cp_609: 'int25' = t_1526
      if cp_609 == 34:
        break
      t_2481 = string_next_2822(source_text_602, i_603)
      i_next_610: 'int25' = t_2481
      end_611: 'int25' = len_2794(source_text_602)
      need_to_flush_612: 'bool22' = False
      if cp_609 != 92:
        t_1546 = cp_609
      else:
        need_to_flush_612 = True
        if not len15(source_text_602) > i_next_610:
          expected_token_error_305(source_text_602, i_next_610, out_604, 'escape sequence')
          return_263 = -1
          fn_605.break_()
        t_1530 = string_get_2821(source_text_602, i_next_610)
        esc0_614: 'int25' = t_1530
        t_2486 = string_next_2822(source_text_602, i_next_610)
        i_next_610 = t_2486
        if esc0_614 == 34:
          t_1533 = True
        else:
          if esc0_614 == 92:
            t_1532 = True
          else:
            t_1532 = esc0_614 == 47
          t_1533 = t_1532
        if t_1533:
          t_1544 = esc0_614
        elif esc0_614 == 98:
          t_1544 = 8
        elif esc0_614 == 102:
          t_1544 = 12
        elif esc0_614 == 110:
          t_1544 = 10
        elif esc0_614 == 114:
          t_1544 = 13
        elif esc0_614 == 116:
          t_1544 = 9
        elif esc0_614 == 117:
          if string_has_at_least_2826(source_text_602, i_next_610, end_611, 4):
            start_hex_616: 'int25' = i_next_610
            t_2488 = string_next_2822(source_text_602, i_next_610)
            i_next_610 = t_2488
            t_2489 = string_next_2822(source_text_602, i_next_610)
            i_next_610 = t_2489
            t_2490 = string_next_2822(source_text_602, i_next_610)
            i_next_610 = t_2490
            t_2491 = string_next_2822(source_text_602, i_next_610)
            i_next_610 = t_2491
            t_2492 = decode_hex_unsigned_312(source_text_602, start_hex_616, i_next_610)
            t_1541 = t_2492
          else:
            t_1541 = -1
          hex_615: 'int25' = t_1541
          if hex_615 < 0:
            expected_token_error_305(source_text_602, i_next_610, out_604, 'four hex digits')
            return_263 = -1
            fn_605.break_()
          t_1542 = hex_615
          t_1544 = t_1542
        else:
          expected_token_error_305(source_text_602, i_next_610, out_604, 'escape sequence')
          return_263 = -1
          fn_605.break_()
        t_1546 = t_1544
      decoded_cp_613: 'int25' = t_1546
      if lead_surrogate_607 >= 0:
        need_to_flush_612 = True
        lead_617: 'int25' = lead_surrogate_607
        if 56320 <= decoded_cp_613:
          t_1547 = decoded_cp_613 <= 57343
        else:
          t_1547 = False
        if t_1547:
          lead_surrogate_607 = -1
          t_1548 = (lead_617 - 55296) * 1024 | decoded_cp_613 - 56320
          decoded_cp_613 = 65536 + t_1548
      else:
        if 55296 <= decoded_cp_613:
          t_1549 = decoded_cp_613 <= 56319
        else:
          t_1549 = False
        if t_1549:
          need_to_flush_612 = True
      if need_to_flush_612:
        sb_606.append(source_text_602[consumed_608 : i_603])
        if lead_surrogate_607 >= 0:
          sb_606.append(chr58(lead_surrogate_607))
        if 55296 <= decoded_cp_613:
          t_1550 = decoded_cp_613 <= 56319
        else:
          t_1550 = False
        if t_1550:
          lead_surrogate_607 = decoded_cp_613
        else:
          lead_surrogate_607 = -1
          sb_606.append(chr58(decoded_cp_613))
        consumed_608 = i_next_610
      i_603 = i_next_610
    if not len15(source_text_602) > i_603:
      t_1555 = True
    else:
      t_1554 = string_get_2821(source_text_602, i_603)
      t_1555 = t_1554 != 34
    if t_1555:
      expected_token_error_305(source_text_602, i_603, out_604, '"')
      return_263 = -1
    else:
      if lead_surrogate_607 >= 0:
        sb_606.append(chr58(lead_surrogate_607))
      else:
        sb_606.append(source_text_602[consumed_608 : i_603])
      t_2510 = string_next_2822(source_text_602, i_603)
      i_603 = t_2510
      t_2512 = ''.join(sb_606)
      out_604.string_value(t_2512)
      return_263 = i_603
  return return_263
def parse_json_object_309(source_text_591: 'str21', i_592: 'int25', out_593: 'JsonProducer') -> 'int25':
  return_261: 'int25'
  t_2441: 'int25'
  t_2442: 'int25'
  t_2449: 'int25'
  t_2452: 'int25'
  t_2461: 'int25'
  t_2464: 'int25'
  t_2465: 'int25'
  t_1479: 'int25'
  t_1480: 'bool22'
  t_1486: 'int25'
  t_1487: 'bool22'
  t_1492: 'int25'
  t_1497: 'int25'
  t_1498: 'bool22'
  t_1504: 'int25'
  t_1510: 'int25'
  t_1511: 'bool22'
  t_1515: 'int25'
  t_1516: 'bool22'
  with Label34() as fn_594:
    if not len15(source_text_591) > i_592:
      t_1480 = True
    else:
      t_1479 = string_get_2821(source_text_591, i_592)
      t_1480 = t_1479 != 123
    if t_1480:
      expected_token_error_305(source_text_591, i_592, out_593, "'{'")
      return_261 = -1
      fn_594.break_()
    out_593.start_object()
    t_2441 = string_next_2822(source_text_591, i_592)
    t_2442 = skip_json_spaces_307(source_text_591, t_2441)
    i_592 = t_2442
    if len15(source_text_591) > i_592:
      t_1486 = string_get_2821(source_text_591, i_592)
      t_1487 = t_1486 != 125
    else:
      t_1487 = False
    if t_1487:
      while True:
        after_key_595: 'int25' = parse_json_string_311(source_text_591, i_592, out_593)
        if not after_key_595 >= 0:
          return_261 = -1
          fn_594.break_()
        t_1492 = require_string_index59(after_key_595)
        t_2449 = skip_json_spaces_307(source_text_591, t_1492)
        i_592 = t_2449
        if len15(source_text_591) > i_592:
          t_1497 = string_get_2821(source_text_591, i_592)
          t_1498 = t_1497 == 58
        else:
          t_1498 = False
        if t_1498:
          t_2452 = string_next_2822(source_text_591, i_592)
          i_592 = t_2452
          after_property_value_596: 'int25' = parse_json_value_308(source_text_591, i_592, out_593)
          if not after_property_value_596 >= 0:
            return_261 = -1
            fn_594.break_()
          t_1504 = require_string_index59(after_property_value_596)
          i_592 = t_1504
        else:
          expected_token_error_305(source_text_591, i_592, out_593, "':'")
          return_261 = -1
          fn_594.break_()
        t_2461 = skip_json_spaces_307(source_text_591, i_592)
        i_592 = t_2461
        if len15(source_text_591) > i_592:
          t_1510 = string_get_2821(source_text_591, i_592)
          t_1511 = t_1510 == 44
        else:
          t_1511 = False
        if t_1511:
          t_2464 = string_next_2822(source_text_591, i_592)
          t_2465 = skip_json_spaces_307(source_text_591, t_2464)
          i_592 = t_2465
        else:
          break
    if len15(source_text_591) > i_592:
      t_1515 = string_get_2821(source_text_591, i_592)
      t_1516 = t_1515 == 125
    else:
      t_1516 = False
    if t_1516:
      out_593.end_object()
      return_261 = string_next_2822(source_text_591, i_592)
    else:
      expected_token_error_305(source_text_591, i_592, out_593, "'}'")
      return_261 = -1
  return return_261
def parse_json_array_310(source_text_597: 'str21', i_598: 'int25', out_599: 'JsonProducer') -> 'int25':
  return_262: 'int25'
  t_2416: 'int25'
  t_2417: 'int25'
  t_2425: 'int25'
  t_2428: 'int25'
  t_2429: 'int25'
  t_1451: 'int25'
  t_1452: 'bool22'
  t_1458: 'int25'
  t_1459: 'bool22'
  t_1464: 'int25'
  t_1470: 'int25'
  t_1471: 'bool22'
  t_1475: 'int25'
  t_1476: 'bool22'
  with Label34() as fn_600:
    if not len15(source_text_597) > i_598:
      t_1452 = True
    else:
      t_1451 = string_get_2821(source_text_597, i_598)
      t_1452 = t_1451 != 91
    if t_1452:
      expected_token_error_305(source_text_597, i_598, out_599, "'['")
      return_262 = -1
      fn_600.break_()
    out_599.start_array()
    t_2416 = string_next_2822(source_text_597, i_598)
    t_2417 = skip_json_spaces_307(source_text_597, t_2416)
    i_598 = t_2417
    if len15(source_text_597) > i_598:
      t_1458 = string_get_2821(source_text_597, i_598)
      t_1459 = t_1458 != 93
    else:
      t_1459 = False
    if t_1459:
      while True:
        after_element_value_601: 'int25' = parse_json_value_308(source_text_597, i_598, out_599)
        if not after_element_value_601 >= 0:
          return_262 = -1
          fn_600.break_()
        t_1464 = require_string_index59(after_element_value_601)
        i_598 = t_1464
        t_2425 = skip_json_spaces_307(source_text_597, i_598)
        i_598 = t_2425
        if len15(source_text_597) > i_598:
          t_1470 = string_get_2821(source_text_597, i_598)
          t_1471 = t_1470 == 44
        else:
          t_1471 = False
        if t_1471:
          t_2428 = string_next_2822(source_text_597, i_598)
          t_2429 = skip_json_spaces_307(source_text_597, t_2428)
          i_598 = t_2429
        else:
          break
    if len15(source_text_597) > i_598:
      t_1475 = string_get_2821(source_text_597, i_598)
      t_1476 = t_1475 == 93
    else:
      t_1476 = False
    if t_1476:
      out_599.end_array()
      return_262 = string_next_2822(source_text_597, i_598)
    else:
      expected_token_error_305(source_text_597, i_598, out_599, "']'")
      return_262 = -1
  return return_262
def after_substring_315(string_640: 'str21', in_string_641: 'int25', substring_642: 'str21') -> 'int25':
  return_267: 'int25'
  t_2409: 'int25'
  t_2410: 'int25'
  t_1446: 'int25'
  t_1447: 'int25'
  with Label34() as fn_643:
    i_644: 'int25' = in_string_641
    j_645: 'int25' = 0
    while True:
      if not len15(substring_642) > j_645:
        break
      if not len15(string_640) > i_644:
        return_267 = -1
        fn_643.break_()
      t_1446 = string_get_2821(string_640, i_644)
      t_1447 = string_get_2821(substring_642, j_645)
      if t_1446 != t_1447:
        return_267 = -1
        fn_643.break_()
      t_2409 = string_next_2822(string_640, i_644)
      i_644 = t_2409
      t_2410 = string_next_2822(substring_642, j_645)
      j_645 = t_2410
    return_267 = i_644
  return return_267
def parse_json_boolean_313(source_text_626: 'str21', i_627: 'int25', out_628: 'JsonProducer') -> 'int25':
  return_265: 'int25'
  t_2397: 'bool22'
  t_1422: 'int25'
  t_1436: 'bool22'
  t_1437: 'str21'
  with Label34() as fn_629:
    ch0_630: 'int25'
    if len15(source_text_626) > i_627:
      t_1422 = string_get_2821(source_text_626, i_627)
      ch0_630 = t_1422
    else:
      ch0_630 = 0
    end_631: 'int25' = len_2794(source_text_626)
    keyword_632: 'Union28[str21, None]'
    n_633: 'int25'
    if ch0_630 == 102:
      keyword_632 = 'false'
      n_633 = 5
    elif ch0_630 == 116:
      keyword_632 = 'true'
      n_633 = 4
    else:
      keyword_632 = None
      n_633 = 0
    if not keyword_632 is None:
      t_2397 = string_has_at_least_2826(source_text_626, i_627, end_631, n_633)
      t_1436 = t_2397
    else:
      t_1436 = False
    if t_1436:
      if keyword_632 is None:
        raise RuntimeError54()
      else:
        t_1437 = keyword_632
      after_634: 'int25' = after_substring_315(source_text_626, i_627, t_1437)
      if after_634 >= 0:
        out_628.boolean_value(n_633 == 4)
        return_265 = after_634
        fn_629.break_()
    expected_token_error_305(source_text_626, i_627, out_628, '`false` or `true`')
    return_265 = -1
  return return_265
def parse_json_null_314(source_text_635: 'str21', i_636: 'int25', out_637: 'JsonProducer') -> 'int25':
  return_266: 'int25'
  with Label34() as fn_638:
    after_639: 'int25' = after_substring_315(source_text_635, i_636, 'null')
    if after_639 >= 0:
      out_637.null_value()
      return_266 = require_string_index59(after_639)
      fn_638.break_()
    expected_token_error_305(source_text_635, i_636, out_637, '`null`')
    return_266 = -1
  return return_266
def parse_json_number_316(source_text_646: 'str21', i_647: 'int25', out_648: 'JsonProducer') -> 'int25':
  return_268: 'int25'
  t_2345: 'int25'
  t_2350: 'int25'
  t_2353: 'int25'
  t_2356: 'int25'
  t_2359: 'int25'
  t_2364: 'int25'
  t_2369: 'int25'
  t_2372: 'int25'
  t_1362: 'int25'
  t_1363: 'bool22'
  t_1366: 'int25'
  t_1368: 'bool22'
  t_1369: 'bool22'
  t_1374: 'float56'
  t_1376: 'int25'
  t_1377: 'bool22'
  t_1379: 'float56'
  t_1380: 'float56'
  t_1382: 'int25'
  t_1383: 'bool22'
  t_1386: 'int25'
  t_1387: 'bool22'
  t_1389: 'float56'
  t_1390: 'float56'
  t_1392: 'int25'
  t_1393: 'int25'
  t_1394: 'bool22'
  t_1398: 'bool22'
  t_1401: 'int25'
  t_1402: 'bool22'
  t_1404: 'bool22'
  t_1406: 'bool22'
  t_1407: 'bool22'
  t_1408: 'int25'
  t_1410: 'bool22'
  t_1411: 'float56'
  t_1412: 'bool22'
  t_1413: 'bool22'
  with Label34() as fn_649:
    is_negative_650: 'bool22' = False
    start_of_number_651: 'int25' = i_647
    if len15(source_text_646) > i_647:
      t_1362 = string_get_2821(source_text_646, i_647)
      t_1363 = t_1362 == 45
    else:
      t_1363 = False
    if t_1363:
      is_negative_650 = True
      t_2345 = string_next_2822(source_text_646, i_647)
      i_647 = t_2345
    digit0_652: 'int25'
    if len15(source_text_646) > i_647:
      t_1366 = string_get_2821(source_text_646, i_647)
      digit0_652 = t_1366
    else:
      digit0_652 = -1
    if digit0_652 < 48:
      t_1368 = True
    else:
      t_1368 = 57 < digit0_652
    if t_1368:
      error_653: 'str21'
      if not is_negative_650:
        t_1369 = digit0_652 != 46
      else:
        t_1369 = False
      if t_1369:
        error_653 = 'JSON value'
      else:
        error_653 = 'digit'
      expected_token_error_305(source_text_646, i_647, out_648, error_653)
      return_268 = -1
      fn_649.break_()
    t_2350 = string_next_2822(source_text_646, i_647)
    i_647 = t_2350
    n_digits_654: 'int25' = 1
    t_1374 = int_to_float64_2799(digit0_652 - 48)
    tentative_value_655: 'float56' = t_1374
    if 48 != digit0_652:
      while True:
        if not len15(source_text_646) > i_647:
          break
        t_1376 = string_get_2821(source_text_646, i_647)
        possible_digit_656: 'int25' = t_1376
        if 48 <= possible_digit_656:
          t_1377 = possible_digit_656 <= 57
        else:
          t_1377 = False
        if t_1377:
          t_2353 = string_next_2822(source_text_646, i_647)
          i_647 = t_2353
          n_digits_654 = n_digits_654 + 1
          t_1380 = tentative_value_655 * 10.0
          t_1379 = int_to_float64_2799(possible_digit_656 - 48)
          tentative_value_655 = t_1380 + t_1379
        else:
          break
    n_digits_after_point_657: 'int25' = 0
    if len15(source_text_646) > i_647:
      t_1382 = string_get_2821(source_text_646, i_647)
      t_1383 = 46 == t_1382
    else:
      t_1383 = False
    if t_1383:
      t_2356 = string_next_2822(source_text_646, i_647)
      i_647 = t_2356
      after_point_658: 'int25' = i_647
      while True:
        if not len15(source_text_646) > i_647:
          break
        t_1386 = string_get_2821(source_text_646, i_647)
        possible_digit_659: 'int25' = t_1386
        if 48 <= possible_digit_659:
          t_1387 = possible_digit_659 <= 57
        else:
          t_1387 = False
        if t_1387:
          t_2359 = string_next_2822(source_text_646, i_647)
          i_647 = t_2359
          n_digits_654 = n_digits_654 + 1
          n_digits_after_point_657 = n_digits_after_point_657 + 1
          t_1390 = tentative_value_655 * 10.0
          t_1389 = int_to_float64_2799(possible_digit_659 - 48)
          tentative_value_655 = t_1390 + t_1389
        else:
          break
      if generic_eq_2767(i_647, after_point_658):
        expected_token_error_305(source_text_646, i_647, out_648, 'digit')
        return_268 = -1
        fn_649.break_()
    n_exponent_digits_660: 'int25' = 0
    if len15(source_text_646) > i_647:
      t_1392 = string_get_2821(source_text_646, i_647)
      t_1393 = t_1392 | 32
      t_1394 = 101 == t_1393
    else:
      t_1394 = False
    if t_1394:
      t_2364 = string_next_2822(source_text_646, i_647)
      i_647 = t_2364
      if not len15(source_text_646) > i_647:
        expected_token_error_305(source_text_646, i_647, out_648, 'sign or digit')
        return_268 = -1
        fn_649.break_()
      after_e_661: 'int25'
      after_e_661 = string_get_2821(source_text_646, i_647)
      if after_e_661 == 43:
        t_1398 = True
      else:
        t_1398 = after_e_661 == 45
      if t_1398:
        t_2369 = string_next_2822(source_text_646, i_647)
        i_647 = t_2369
      while True:
        if not len15(source_text_646) > i_647:
          break
        t_1401 = string_get_2821(source_text_646, i_647)
        possible_digit_662: 'int25' = t_1401
        if 48 <= possible_digit_662:
          t_1402 = possible_digit_662 <= 57
        else:
          t_1402 = False
        if t_1402:
          t_2372 = string_next_2822(source_text_646, i_647)
          i_647 = t_2372
          n_exponent_digits_660 = n_exponent_digits_660 + 1
        else:
          break
      if n_exponent_digits_660 == 0:
        expected_token_error_305(source_text_646, i_647, out_648, 'exponent digit')
        return_268 = -1
        fn_649.break_()
    after_exponent_663: 'int25' = i_647
    if n_exponent_digits_660 == 0:
      t_1404 = n_digits_after_point_657 == 0
    else:
      t_1404 = False
    if t_1404:
      value_664: 'float56'
      if is_negative_650:
        value_664 = -tentative_value_655
      else:
        value_664 = tentative_value_655
      if n_digits_654 <= 10:
        if float_lt_eq_2828(-2.147483648E9, value_664):
          t_1406 = float_lt_eq_2828(value_664, 2.147483647E9)
        else:
          t_1406 = False
        t_1407 = t_1406
      else:
        t_1407 = False
      if t_1407:
        t_1408 = float64_to_int_2801(value_664)
        out_648.int_value(t_1408)
        return_268 = i_647
        fn_649.break_()
    numeric_token_string_665: 'str21' = source_text_646[start_of_number_651 : i_647]
    double_value_666: 'float56' = nan60
    if n_exponent_digits_660 != 0:
      t_1410 = True
    else:
      t_1410 = n_digits_after_point_657 != 0
    if t_1410:
      try:
        t_1411 = string_to_float64_2803(numeric_token_string_665)
        double_value_666 = t_1411
      except Exception39:
        pass
    if float_not_eq_2829(double_value_666, -inf61):
      if float_not_eq_2829(double_value_666, inf61):
        t_1412 = float_not_eq_2829(double_value_666, nan60)
      else:
        t_1412 = False
      t_1413 = t_1412
    else:
      t_1413 = False
    if t_1413:
      out_648.float64_value(double_value_666)
    else:
      out_648.numeric_token_value(numeric_token_string_665)
    return_268 = i_647
  return return_268
def parse_json_to_producer(source_text_579: 'str21', out_580: 'JsonProducer') -> 'None':
  t_2319: 'int25'
  t_2321: 'bool22'
  t_2323: 'int25'
  t_2324: 'str21'
  t_1339: 'int25'
  t_1346: 'bool22'
  i_582: 'int25' = 0
  after_value_583: 'int25' = parse_json_value_308(source_text_579, i_582, out_580)
  if after_value_583 >= 0:
    t_1339 = require_string_index59(after_value_583)
    t_2319 = skip_json_spaces_307(source_text_579, t_1339)
    i_582 = t_2319
    if len15(source_text_579) > i_582:
      t_2321 = isinstance32(out_580, JsonParseErrorReceiver)
      t_1346 = t_2321
    else:
      t_1346 = False
    if t_1346:
      t_2323 = len_2794(source_text_579)
      t_2324 = source_text_579[i_582 : t_2323]
      store_json_error_306(out_580, str_cat_2779('Extraneous JSON `', t_2324, '`'))
def parse_json(source_text_667: 'str21') -> 'JsonSyntaxTree':
  p_669: 'JsonSyntaxTreeProducer' = JsonSyntaxTreeProducer()
  parse_json_to_producer(source_text_667, p_669)
  return p_669.to_json_syntax_tree()
def boolean_json_adapter() -> 'JsonAdapter[bool22]':
  return BooleanJsonAdapter_143()
def float64_json_adapter() -> 'JsonAdapter[float56]':
  return Float64JsonAdapter_146()
def int_json_adapter() -> 'JsonAdapter[int25]':
  return IntJsonAdapter_149()
def string_json_adapter() -> 'JsonAdapter[str21]':
  return StringJsonAdapter_152()
t = TypeVar26('t', bound = Any30)
def list_json_adapter(adapter_for_t_735: 'JsonAdapter[t]') -> 'JsonAdapter[(Sequence24[t])]':
  return ListJsonAdapter_155(adapter_for_t_735)
