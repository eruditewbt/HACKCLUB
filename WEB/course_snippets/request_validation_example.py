from pydantic import BaseModel, ValidationError, conint


class InferenceInput(BaseModel):
    age: conint(ge=0, le=120)
    income: float


def main():
    try:
        item = InferenceInput(age=36, income=55000.0)
        print("valid:", item.model_dump())
    except ValidationError as exc:
        print("validation failed:", exc)


if __name__ == "__main__":
    main()
