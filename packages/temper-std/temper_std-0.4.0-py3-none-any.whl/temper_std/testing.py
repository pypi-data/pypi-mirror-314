from temper_core import LoggingConsole as LoggingConsole37, Pair as Pair0, list_join as list_join7, list_map as list_map36, list_get as list_get10
from builtins import bool as bool22, str as str21, type as type38, Exception as Exception39, int as int25, tuple as tuple19, list as list18, len as len15
from typing import MutableSequence as MutableSequence31, Callable as Callable23, Sequence as Sequence24, Union as Union28
from temper_std.regex import str_cat_2779
tuple_2785 = tuple19
list_join_2787 = list_join7
list_2788 = list18
pair_2789 = Pair0
list_map_2790 = list_map36
len_2791 = len15
list_get_2792 = list_get10
console_90: 'LoggingConsole37' = LoggingConsole37(__name__)
class Test:
  passing_16: 'bool22'
  failed_on_assert_17: 'bool22'
  has_unhandled_fail_18: 'bool22'
  failed_on_assert_57: 'bool22'
  passing_58: 'bool22'
  messages_59: 'MutableSequence31[str21]'
  __slots__ = ('passing_16', 'failed_on_assert_17', 'has_unhandled_fail_18', 'failed_on_assert_57', 'passing_58', 'messages_59')
  def assert_(this_7, success_35: 'bool22', message_36: 'Callable23[[], str21]') -> 'None':
    t_280: 'str21'
    if not success_35:
      this_7.passing_58 = False
      t_280 = message_36()
      this_7.messages_59.append(t_280)
  def assert_hard(this_8, success_39: 'bool22', message_40: 'Callable23[[], str21]') -> 'None':
    this_8.assert_(success_39, message_40)
    if not success_39:
      this_8.failed_on_assert_57 = True
      assert False, str21(this_8.messages_combined())
  def soft_fail_to_hard(this_9) -> 'None':
    if this_9.has_unhandled_fail:
      this_9.failed_on_assert_57 = True
      assert False, str21(this_9.messages_combined())
  @property
  def passing(this_11) -> 'bool22':
    return this_11.passing_58
  def messages(this_12) -> 'Sequence24[str21]':
    return tuple_2785(this_12.messages_59)
  @property
  def failed_on_assert(this_13) -> 'bool22':
    return this_13.failed_on_assert_57
  @property
  def has_unhandled_fail(this_14) -> 'bool22':
    t_166: 'bool22'
    if this_14.failed_on_assert_57:
      t_166 = True
    else:
      t_166 = this_14.passing_58
    return not t_166
  def messages_combined(this_15) -> 'Union28[str21, None]':
    return_29: 'Union28[str21, None]'
    t_269: 'Union28[str21, None]'
    if not this_15.messages_59:
      return_29 = None
    else:
      def fn_265(it_56: 'str21') -> 'str21':
        return it_56
      t_269 = list_join_2787(this_15.messages_59, ', ', fn_265)
      return_29 = t_269
    return return_29
  def __init__(this_19) -> None:
    this_19.failed_on_assert_57 = False
    this_19.passing_58 = True
    t_262: 'MutableSequence31[str21]' = list_2788()
    this_19.messages_59 = t_262
test_name: 'type38' = ('<<lang.temper.value.TType: Type, lang.temper.value.Value: String: Type>>', NotImplemented)[1]
test_fun: 'type38' = ('<<lang.temper.value.TType: Type, lang.temper.value.Value: fn (Test): (Void | Bubble): Type>>', NotImplemented)[1]
test_case: 'type38' = ('<<lang.temper.value.TType: Type, lang.temper.value.Value: Pair<String, fn (Test): (Void | Bubble)>: Type>>', NotImplemented)[1]
test_failure_message: 'type38' = ('<<lang.temper.value.TType: Type, lang.temper.value.Value: String: Type>>', NotImplemented)[1]
test_result: 'type38' = ('<<lang.temper.value.TType: Type, lang.temper.value.Value: Pair<String, List<String>>: Type>>', NotImplemented)[1]
def process_test_cases(test_cases_61: 'Sequence24[(Pair0[str21, (Callable23[[Test], None])])]') -> 'Sequence24[(Pair0[str21, (Sequence24[str21])])]':
  def fn_258(test_case_63: 'Pair0[str21, (Callable23[[Test], None])]') -> 'Pair0[str21, (Sequence24[str21])]':
    t_251: 'bool22'
    t_253: 'Sequence24[str21]'
    t_149: 'bool22'
    key_65: 'str21' = test_case_63.key
    fun_66: 'Callable23[[Test], None]' = test_case_63.value
    test_67: 'Test' = Test()
    had_bubble_68: 'bool22'
    try:
      fun_66(test_67)
      had_bubble_68 = False
    except Exception39:
      had_bubble_68 = True
    messages_69: 'Sequence24[str21]' = test_67.messages()
    failures_70: 'Sequence24[str21]'
    if test_67.passing:
      failures_70 = ()
    else:
      if had_bubble_68:
        t_251 = test_67.failed_on_assert
        t_149 = not t_251
      else:
        t_149 = False
      if t_149:
        all_messages_71: 'MutableSequence31[str21]' = list_2788(messages_69)
        all_messages_71.append('Bubble')
        t_253 = tuple_2785(all_messages_71)
        failures_70 = t_253
      else:
        failures_70 = messages_69
    return pair_2789(key_65, failures_70)
  return list_map_2790(test_cases_61, fn_258)
def report_test_results(test_results_72: 'Sequence24[(Pair0[str21, (Sequence24[str21])])]') -> 'None':
  t_235: 'int25'
  t_238: 'str21'
  t_242: 'str21'
  t_135: 'Pair0[str21, (Sequence24[str21])]'
  i_74: 'int25' = 0
  while True:
    t_235 = len_2791(test_results_72)
    if not i_74 < t_235:
      break
    t_135 = list_get_2792(test_results_72, i_74)
    test_result_75: 'Pair0[str21, (Sequence24[str21])]' = t_135
    failure_messages_76: 'Sequence24[str21]' = test_result_75.value
    if not failure_messages_76:
      t_238 = test_result_75.key
      console_90.log(str_cat_2779(t_238, ': Passed'))
    else:
      def fn_234(it_78: 'str21') -> 'str21':
        return it_78
      message_77: 'str21' = list_join_2787(failure_messages_76, ', ', fn_234)
      t_242 = test_result_75.key
      console_90.log(str_cat_2779(t_242, ': Failed ', message_77))
    i_74 = i_74 + 1
def run_test_cases(test_cases_79: 'Sequence24[(Pair0[str21, (Callable23[[Test], None])])]') -> 'None':
  report_test_results(process_test_cases(test_cases_79))
def run_test(test_fun_81: 'Callable23[[Test], None]') -> 'None':
  test_83: 'Test' = Test()
  test_fun_81(test_83)
  test_83.soft_fail_to_hard()
