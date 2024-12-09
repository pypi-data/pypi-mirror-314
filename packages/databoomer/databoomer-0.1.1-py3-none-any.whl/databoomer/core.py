# src/DataBoomer/core.py
import pyperclip
import codecs
import dill
from string import Template

class DataBoomer:
    """
    A tool for serializing Python objects and creating self-contained code snippets
    that can recreate them in any Jupyter notebook.

    Usage:
        db = DataBoomer(my_object, comment="My important data")
        # Automatically copies code to clipboard that can recreate my_object
    """

    def __init__(self, obj, template=None, obj_name=None, comment=None):
        """
        Initialize DataBoomer with an object to serialize.

        Args:
            obj: Any Python object that can be serialized by dill
            template (Template, optional): Custom template for the output code
            obj_name (str, optional): Name to use for the object in generated code
            comment (str, optional): Comment to include with the generated code
        """
        # Store the object we want to serialize
        self.obj = obj
        # Store or default the comment
        self.comment = comment or ''
        
        # Default template for generating the code snippet
        default_template = Template(
            "# comment: $comment\n"
            "payload = '''$payload'''\n"
            "$obj_name = dill.loads(codecs.decode(payload.encode(), 'base64'))"
        )
        self.template = template or default_template

        # Try to automatically detect the object's variable name, or use provided one
        self.obj_name = obj_name or self.instance_name()
        
        # Will store the final code snippet
        self.payload = ''
        
        # Generate and copy the code immediately
        self.encode()
        self.boom()

    def instance_name(self):
        """
        Try to automatically detect the variable name of the object in the current scope.
        
        Returns:
            str: The variable name if found, otherwise 'obj'
        """
        for name, value in globals().items():
            if value is self.obj:
                return name
        return 'obj'  # Fallback if name not found

    def encode(self):
        """
        Serialize the object and create the code snippet.
        
        The process:
        1. Serialize object using dill
        2. Encode to base64
        3. Create a single-line string (removes newlines)
        4. Insert into the template
        """
        # Serialize and encode the object
        serialized = dill.dumps(self.obj)
        encoded = codecs.encode(serialized, "base64")
        # Create single-line string without newlines
        payload = encoded.decode().replace('\n', '')
        
        # Generate the final code using the template
        self.payload = self.template.substitute(
            comment=self.comment,
            payload=payload,
            obj_name=self.obj_name
        )

    def boom(self):
        """
        Copy the generated code snippet to the clipboard.
        """
        pyperclip.copy(self.payload)