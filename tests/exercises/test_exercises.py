from http import HTTPStatus

import pytest

from clients.exercises.exercises_client import ExercisesClient
from fixtures.courses import CourseFixture
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, ExerciseResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.exercises import assert_create_exercise_response


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
