class Text:
    def __init__(self, text: str = None, file = None):
        """
        Initialization for the class.
        
        ## Parameters:
        text (str): The text to be stored in the object.
        file: The file to read. Optional.
        """
        if text:
            self.text = text
        elif file:
            self.text = open(file).read()
        else:
            raise ValueError("Please specify either text or file!")

    def reverse(self) -> str:
        """
        Reverses the text stored in the object.

        ## Returns:
        output (str): The reversed text.
        """
        return self.text[::-1]

    def __repr__(self) -> str:
        """
        Provides a string representation of the object.

        ## Returns:
        str: A string that represents the object.
        """
        return f"Text(text='{self.text}')"
    
    def alter_case(self) -> str:
        """
        Alters the case of the text so it alternates between lowercase and uppercase.

        ## Returns:
        altered (str): The altered text with alternating case.
        """
        altered = ""
        for i, letter in enumerate(self.text):
            if i % 2 == 0:
                altered += letter.lower()
            else:
                altered += letter.upper()
        return altered
    
    def shuffle(self) -> str:
        """
        Shuffles the text.

        ## Returns:
        shuffled (str): The shuffled text.
        """

        text_list = list(self.text)
        import random
        random.shuffle(text_list)
        shuffled = "".join(text_list)
        shuffled = " ".join(shuffled.split())
        return shuffled

    def trim_spaces(self) -> str:
        """
        Removes duplicate spaces. (If your text contains spaces like these: "Exa mple  text", only the longer spaces will be removed, Python being Python)

        ## Returns:
        output (str): Cleaned up text.
        """
        words = self.text.split()
        output = " ".join(words)
        return output
    
    def is_palindrome(self) -> bool:
        """
        Checks if the text is a palindrome.

        ## Returns:
        is_palindrome (bool): Wether the text is a palindrome or not.
        """

        cleaned_text = "".join(self.text.lower().split())
        return cleaned_text == cleaned_text[::-1]
    
    def remove_html(self) -> str:
        """
        Removes HTML tags.

        ## Returns:
        removed_html (str): The text without any HTML tags.
        """
        import re
        return re.sub(r'<[^>]*>', '', self.text)
        