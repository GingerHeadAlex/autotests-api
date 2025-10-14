from http import HTTPStatus

import pytest

from clients.exercises.exercises_client import ExercisesClient
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, ExerciseResponseSchema, \
    UpdateExerciseRequestSchema, UpdateExerciseResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, \
    assert_update_exercise_response, assert_exercise_not_found_response
from clients.errors_schema import InternalErrorResponseSchema

@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
    def test_create_exercise(
            self,
            exercises_client: ExercisesClient,
            function_course: CourseFixture
    ):
        request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
        # Отправляем запрос на создание задания курса
        response = exercises_client.create_exercise_api(request)
        # Преобразуем JSON-ответ в объект схемы
        response_data = ExerciseResponseSchema.model_validate_json(response.text)
        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что данные в ответе соответствуют запросу
        assert_create_exercise_response(request, response_data)
        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture):
        # Отправляем запрос на получение задания курса
        response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        # Преобразуем JSON-ответ в объект схемы
        response_data = ExerciseResponseSchema.model_validate_json(response.text)
        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что данные в ответе соответствуют запросу
        assert_get_exercise_response(response_data,function_exercise.response)
        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        request = UpdateExerciseRequestSchema()
        response = exercises_client.update_exercise_api(function_exercise.response.exercise.id, request)
        # Преобразуем JSON-ответ в объект схемы
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что данные в ответе соответствуют запросу
        assert_update_exercise_response(request,response_data)
        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_delete_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        # Отправляем запрос на удаление задания курса
        delete_response = exercises_client.delete_exercise_api(function_exercise.response.exercise.id)
        # Проверяем статус-код ответа
        assert_status_code(delete_response.status_code, HTTPStatus.OK)
        # Пытаемся получить удаленное задание
        get_response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)
        # Проверяем, что сервер вернул 404 Not Found
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        # Проверяем, что в ответе содержится ошибка "Exercise not found"
        assert_exercise_not_found_response(get_response_data)
        # Валидируем JSON-схему ответа
        validate_json_schema(get_response.json(), get_response_data.model_json_schema())
