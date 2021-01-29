class Job:

    def __init__(self, company, job_title, post_url, location, description):
        self.company = company
        self.job_title = job_title
        self.post_url = post_url
        self.location = location
        self.description = description

    def get_info(self):
        print(f"{self.job_title} - {self.company}")

    def as_dict(self) -> dict:
        """
        Method to convert a job obj to a dict for pandas
        :return:
        """
        return dict(
            title=self.job_title,
            company=self.company,
            location=self.location,
            post_url=self.post_url,
            description=self.description
        )

