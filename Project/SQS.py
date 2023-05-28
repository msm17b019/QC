class Sqs:
    def __init__(self, sqs_resource) -> None:
        """Class that represents Amazon SQS service.

        Args:
            sqs_resource : SQS resource to create, manage and configure AWS SQS service at high level
        """
        self.sqs_resource = sqs_resource

    def create_sqs_queue(self, name: str, tags: dict) -> None:
        """This method creates SQS queue.

        Args:
            name (str): Name of the queue.
            tags (dict): Tags to add to the queue.
        """
        if self.check_sqs_queue(name):
            self.sqs_resource.create_queue(QueueName=name, tags=tags)

    def check_sqs_queue(self, name: str) -> bool:
        """To check whether SQS already exists with the given name.

        Args:
            name (str): Name of the queue to check.

        Returns:
            bool : False if queue exists with the given name, else True.
        """
        for queue in self.sqs_resource.queues.all():
            if name == queue.attributes['QueueArn'].split(':')[-1]:
                return False
        else:
            return True