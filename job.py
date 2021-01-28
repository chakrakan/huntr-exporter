class Job:

    def __init__(self, company, job_title, post_url, location, description):
        self.company = company
        self.job_title = job_title
        self.post_url = post_url
        self.location = location
        self.description = description

    def get_info(self):
        print(f"{self.job_title} - {self.company}")
