class FindingFiveStudyStoreUser:
    def __init__(self, userID, numCredits=0, ownedStudies=[], viewedStudies=[], wishList=[], authorList=[]):
        self.userID = userID
        self.numCredits = numCredits
        self.ownedStudies = ownedStudies  # list of FFSS studies
        self.viewedStudies = viewedStudies  # list of FFSS studies
        self.wishList = wishList  # wish list of FFSS studies
        self.authorList = authorList

    def build_database_doc(self):
        returner = dict()
        returner['User_id'] = self.userID
        returner['Num Credits'] = self.numCredits
        returner['Owned Studies'] = self.ownedStudies
        returner['Viewed Studies'] = self.viewedStudies
        returner['Wish List'] = self.wishList
        returner['Author List'] = self.authorList
        return returner

    def get_userId(self):
        return self.userID

    def get_numCredits(self):
        return self.numCredits

    def get_ownedStudies(self):
        return self.ownedStudies

    def get_viewedStudies(self):
        return self.viewedStudies

    def get_wishList(self):
        return self.wishList

    def get_authorList(self):
        return self.authorList


