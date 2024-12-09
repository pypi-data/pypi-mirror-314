from sample_ds_project.logging import logger

STAGE_NAME = "Model Evaluation Stage"


class ModelEvaluationPipeline:
    def __init__(self) -> None:
        """
        This class shall be used for model evaluation pipeline.

        __init__ is the constructor method of class.
        """
        pass

    def run(self) -> None:
        """
        This method executes the main model evaluation pipeline process.

        It orchestrates the model evaluation tasks to evaluate the model
        using the data prepared in the previous stages.
        """
        pass


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelEvaluationPipeline()
        obj.run()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise
