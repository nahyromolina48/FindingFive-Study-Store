class FindingFiveStudyStoreStudy:
    def __init__(self, id, title, author, cost, purpose, references, categories, subcategories, keywords, num_stimuli,
                 num_responses, randomize, duration, num_trials, rating, institution, template, images, abstract, author_id, upload_date=None):
        self.studyID = id
        self.title = title
        self.author = author
        self.costInCredits = cost
        self.purpose = purpose
        self.references = references
        self.categories = categories
        self.subcategories = subcategories
        self.keywords = keywords
        self.num_stimuli = num_stimuli
        self.num_responses = num_responses
        self.num_trials = num_trials
        self.randomize = randomize
        self.duration = duration
        self.rating = rating
        self.institution = institution
        self.template = template
        self.images = images
        self.abstract = abstract
        self.author_id = author_id
        self.upload_date = upload_date

    def build_dict(self):
        returner = dict()
        returner['studyID'] = self.studyID
        returner['title'] = self.title
        returner['author'] = self.author
        returner['costInCredits'] = self.costInCredits
        returner['purpose'] = self.purpose
        returner['references'] = self.references
        returner['categories'] = self.categories
        returner['subcategories'] = self.subcategories
        returner['keywords'] = self.keywords
        returner['num_stimuli'] = self.num_stimuli
        returner['num_responses'] = self.num_responses
        returner['num_trials'] = self.num_trials
        returner['randomize'] = self.randomize
        returner['duration'] = self.duration
        returner['rating'] = self.rating
        returner['institution'] = self.institution
        returner['template'] = self.template
        returner["images"] = self.images
        returner["abstract"] = self.abstract
        returner["authorID"] = self.author_id
        if self.upload_date is not None:
            returner["upload_date"] = self.upload_date
        return returner

    def build_database_doc(self):
        returner = dict()
        returner['Study_id'] = self.studyID
        returner['Title'] = self.title
        returner['Author'] = self.author
        returner['CostinCredits'] = self.costInCredits
        returner['Purpose'] = self.purpose
        returner['References'] = self.references
        returner['Categories'] = self.categories
        returner['Sub_Categories'] = self.subcategories
        returner['Keywords'] = self.keywords
        returner['Num_Stimuli'] = self.num_stimuli
        returner['Num_Responses'] = self.num_responses
        returner['Num_trials'] = self.num_trials
        returner['Randomize'] = self.randomize
        returner['Duration'] = self.duration
        returner['Rating'] = self.rating
        returner['Institution'] = self.institution
        returner['Template'] = self.template
        returner["Images"] = self.images
        returner["Abstract"] = self.abstract
        returner["Author_id"] = self.author_id
        out = dict()
        out["$set"] = returner
        out["$currentDate"] = {"Upload Date": True}
        return out

    def get_costInCredits(self):
        return self.costInCredits

    def set_template(self, new_template):
        self.template = new_template
