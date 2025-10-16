from clients.exercises.exercises_schema import CreateExerciseRequestSchema,GetExerciseResponseSchema, ExercisesSchema, \
UpdateExerciseRequestSchema, UpdateExerciseResponseSchema, CreateExerciseResponseSchema, GetExercisesResponseSchema
from clients.errors_schema import InternalErrorResponseSchema
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.errors import assert_internal_error_response

def assert_create_exercise_response(
        request: CreateExerciseRequestSchema,
        response: CreateExerciseResponseSchema
):
    """
    Проверяет, что ответ на создание задания курса соответствует данным из запроса.

    :param request: Исходный запрос на создание задания курса.
    :param response: Ответ API с созданным заданием в курсе.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    # Проверяем основные поля
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.course_id, request.course_id, "course_id")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")

def assert_exercise(
        actual: ExercisesSchema,
        expected: ExercisesSchema):
    """
    Проверяет, что фактические данные задания курса соответствуют ожидаемым.

    :param actual: Фактические данные задания курса.
    :param expected: Ожидаемые данные задания курса.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.course_id, expected.course_id, "course_id")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.order_index, expected.order_index, "order_index")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")

def assert_get_exercise_response(
        get_exercise_response: GetExerciseResponseSchema,
        create_exercise_response: GetExerciseResponseSchema
):
    """
    Проверяет, что ответ на получение упражнения соответствует ответу на его создание.

    :param get_exercise_response: Ответ API при запросе данных упражнения.
    :param create_exercise_response: Ответ API при создании упражнения.
    :raises AssertionError: Если данные упражнения не совпадают.
    """
    assert_exercise(get_exercise_response.exercise, create_exercise_response.exercise)


def assert_update_exercise_response(
        request: UpdateExerciseRequestSchema,
        response: UpdateExerciseResponseSchema
):
    """
    Проверяет, что ответ на обновление задания курса соответствует данным из запроса.

    :param request: Исходный запрос на обновление задания курса.
    :param response: Ответ API с обновленными данными задания курса.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """

    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")

def assert_exercise_not_found_response(
        actual: InternalErrorResponseSchema
):
    """
    Функция для проверки ошибки, если задание не найдено на сервере.

    :param actual: Фактический ответ.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Exercise not found"
    """
    # Ожидаемое сообщение об ошибке, если файл не найден
    expected = InternalErrorResponseSchema(details="Exercise not found")
    # Используем ранее созданную функцию для проверки внутренней ошибки
    assert_internal_error_response(actual, expected)

def assert_get_exercises_response(
        get_exercises_response: GetExercisesResponseSchema,
        create_exercises_responses: list[CreateExerciseResponseSchema]
):
    """
    Проверяет, что ответ на получение списка задания курсов соответствует ответам на их создание.

    :param get_exercises_response: Ответ API при запросе списка заданий курса.
    :param create_exercises_responses: Список API ответов при создании заданий курсов.
    :raises AssertionError: Если данные курсов не совпадают.
    """
    assert_length(get_exercises_response.exercises, create_exercises_responses, "exercises")

    for index, create_exercise_response in enumerate(create_exercises_responses):
        assert_exercise(get_exercises_response.exercises[index], create_exercise_response.exercise)
