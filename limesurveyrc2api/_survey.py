from collections import OrderedDict
import base64
import json
from limesurveyrc2api.exceptions import LimeSurveyError


class _Survey(object):

    def __init__(self, api):
        self.api = api

    def list_surveys(self, username=None):
        """
        List surveys accessible to the specified username.

        Parameters
        :param username: LimeSurvey username to list accessible surveys for.
        :type username: String
        """
        method = "list_surveys"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iSurveyID", username or self.api.username)
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Invalid user",
                "No surveys found",
                "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is list
        return response

    def list_questions(self, survey_id,
                       group_id=None, language=None):
        """
        Return a list of questions from the specified survey.

        Parameters
        :param survey_id: ID of survey to list questions from.
        :type survey_id: Integer
        :param group_id: ID of the question group to filter on.
        :type group_id: Integer
        :param language: Language of survey to return for.
        :type language: String
        """
        method = "list_questions"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iSurveyID", survey_id),
            ("iGroupID", group_id),
            ("sLanguage", language)
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "Error: Invalid language",
                "Error: IMissmatch in surveyid and groupid",
                "No questions found",
                "No permission",
                "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is list
        return response

    def export_responses(self, survey_id, document_type='json'):
        """
        Return a list of responses from the specified survey.
        Parameters
        :param survey_id: ID of survey to list questions from.
        :type survey_id: Integer
        :param language: Language of survey to return for.
        :type language: String
        """
        # string $sSessionKey, int $iSurveyID, string $sDocumentType, string $sLanguageCode = null, 
        # string $sCompletionStatus = 'all', string $sHeadingType = 'code', string $sResponseType = 'short', 
        # integer $iFromResponseID = null, integer $iToResponseID = null, array $aFields = null):
        method = "export_responses"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iSurveyID", survey_id),
            ("$sDocumentType", "json"),
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "Error: Invalid language",
                "No Data, could not get max id.",
                "No permission",
                "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            response = base64.b64decode(response) # to bytes object
            # unescape backslashed ( \u20ac ) unicode characters
            response = response.decode('unicode_escape') # to unicode string
            response = json.loads(response)['responses']
            assert type(response) is list
        return response
