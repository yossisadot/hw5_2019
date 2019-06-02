from typing import Union, Tuple
import pathlib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

class QuestionnaireAnalysis:
    """
    Reads and analyzes data generated by the questionnaire experiment.
    Should be able to accept strings and pathlib.Path objects.
    """
    
    def __init__(self, data_fname: Union[pathlib.Path, str]):
        if not pathlib.Path(data_fname).is_file():
            raise ValueError(f"'{data_fname}' is not a valid file")
        self.data_fname = pathlib.Path(data_fname)
        
    def read_data(self):
        """
        Reads the json data located in self.data_fname into memory, to
        the attribute self.data.
        """
        self.data = pd.read_json(self.data_fname)
        
    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculates and plots the age distribution of the participants.
        Returns a tuple containing two numpy arrays:
        The first item being the number of people in a given bin.
        The second item being the bin edges.
        """
        # Unlike in the instructions, the last bin is close-ended
        age_dist = plt.hist(self.data["age"], bins=np.linspace(0, 100, 11))
        # Plots the age distribution of the participants
        plt.xlabel('Age')
        plt.ylabel('Number of people')
        plt.show()
        return age_dist

    def remove_rows_without_mail(self) -> pd.DataFrame:
        """
        Checks self.data for rows with invalid emails, and removes them.
        Returns the corrected DataFrame, i.e. the same table but with
        the erroneous rows removed and the (ordinal) index after a reset.
        """
        # Creates a corrected copy of the df, because the next func uses the original df
        with_valid_mail = self.data[self.data["email"].str.match(
            r'\w+[.\w+]*@\w+.\w+')].reset_index()
        return with_valid_mail
        
    def fill_na_with_mean(self) -> Union[pd.DataFrame, np.ndarray]:
        """
        Finds, in the original DataFrame, the subjects that didn't answer
        all questions, and replaces that missing value with the mean of the
        other grades for that student. Returns the corrected DataFrame,
        as well as the row indices of the students that their new grades
        were generated.
        """
        # Finds the subjects that didn't answer all questions
        nan_array = np.array(self.data.index[self.data.loc[:,'q1':'q5'].isna().any(1)])
        #########################################################################################
        # Regarding the following 2 lines:                                                      #
        # In line 68 I couldn't find a way to fill by row with one statement that covers all,   #
        # or a range of, collumns at once without specifying each one (except by transpose, but #
        # I don't like it). Since I specify each, I used 'mean_grade' (line 67) for readability #
        #########################################################################################
        mean_grade = self.data.loc[:,'q1':'q5'].mean(axis=1)
        self.data.fillna({'q1':mean_grade, 'q2':mean_grade, 'q3':mean_grade, 'q4':mean_grade, 
            'q5':mean_grade}, inplace=True)
        return self.data, nan_array


    def correlate_gender_age(self) -> pd.DataFrame:
        """
        Looks for a correlation between the gender of the subject, their age
        and the score for all five questions.
        Returns a DataFrame with a MultiIndex containing the gender and whether
        the subject is above 40 years of age, and the average score in each of
        the five questions.
        """
        gender_age=self.data.groupby(['gender', self.data.age > 40])[[
            'q1','q2','q3','q4','q5']].mean()
        ########################################################################################
        # The return data is different from the 'q4_corr.csv' and the 'avg_per_group.png' even #
        # though the test passes successfully (when I print(test.correlate_gender_age()) I get #
        # results different the csv). But I checked the real grouped data and it seems that    #
        # the data from this function is accurate.                                             #
        ########################################################################################
        return gender_age
        

if __name__ == '__main__':
    w = 1
    # test_int=QuestionnaireAnalysis(w)
    x = pathlib.Path('tata.json')
    # test_nofile=QuestionnaireAnalysis(x)
    y = 'data.json'
    test_str=QuestionnaireAnalysis(y)
    z = pathlib.Path('data.json')
    test=QuestionnaireAnalysis(z)
    test.read_data()
    test.show_age_distrib()
    test.remove_rows_without_mail()
    test.fill_na_with_mean()
    print(test.correlate_gender_age())