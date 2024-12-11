class DirectResult:
    """
    A class to represent a result from Anura Direct.
    """

    result = ''
    mobile = None
    rule_sets = []
    invalid_traffic_type = ''

    def __init__(self, result: str, mobile:int|None = None, rule_sets = None, invalid_traffic_type = None):
        self.result = result
        self.mobile = mobile
        self.rule_sets = rule_sets
        self.invalid_traffic_type = invalid_traffic_type
    
    def is_suspect(self) -> bool:
        """
        Returns whether the visitor is deemed to be suspect.
        """

        return self.result == 'suspect'
    
    def is_non_suspect(self) -> bool:
        """
        Returns whether the visitor is deemed to be non-suspect.
        """

        return self.result == 'non-suspect'
    
    def is_mobile(self) -> bool:
        """
        Returns whether the visitor is deemed to be from a mobile device.
        """
        return self.mobile == 1
    
    def __str__(self) -> str:
        return f"DirectResult(result={self.result}, mobile={self.mobile}, rule_sets={self.rule_sets}, invalid_traffic_type={self.invalid_traffic_type})"