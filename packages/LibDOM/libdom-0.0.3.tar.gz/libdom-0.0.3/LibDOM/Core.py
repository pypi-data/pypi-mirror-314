class Element:
    class Inline:
        def __init__(self, *args, **kwargs):
            if "cls" in kwargs:
                kwargs["class"] = kwargs.pop("cls")
            self.args = args
            self.kwargs = kwargs
            
        def __str__(self):
            return self._render()
            
        def _render(self, indent: int = 0):
            indentation = "    " * indent
            result = f"{indentation}<{self.__class__.__name__.lower()}{' '.join(f'{key}=\"{value}\"' for key, value in self.kwargs.items())}/>"
            return result
            
    class BlockLevel:
        def __init__(self, *args, **kwargs):
            if "cls" in kwargs:
                kwargs["class"] = kwargs.pop("cls")
            self.args = args
            self.kwargs = kwargs
            
        def __str__(self):
            return self._render()
            
        def _render(self, indent: int = 0):
            indentation = "    " * indent
            result = f"{indentation}<{self.__class__.__name__.lower()}{' ' if len(self.kwargs) > 0 else ''}{' '.join(f'{key}=\"{value}\"' for key, value in self.kwargs.items())}>"
            
            for arg in self.args:
                if hasattr(arg, '_render'):
                    result += "\n" + arg._render(indent + 1)
                else:
                    result += f"\n{indentation}    {arg}"
                    
            result += f"\n{indentation}</{self.__class__.__name__.lower()}>"
            
            return result

    class Style:
        def __init__(self, styles: dict, *args, **kwargs):
            if "cls" in kwargs:
                kwargs["class"] = kwargs.pop("cls")
            self.args = args
            self.kwargs = kwargs
            self.styles = styles
            
        def __str__(self):
            return self._render(indent=1)
        
        def _render(self, indent=0):
            def process_styles(styles, current_indent=0):
                css_lines = []
                indentation = "    " * (current_indent + 1)
                
                for selector, properties in styles.items():
                    css_lines.append(f"{indentation}{selector} {{")
                    
                    for prop, value in properties.items():
                        if isinstance(value, dict):
                            nested_lines = process_styles(
                                {prop: value}, current_indent + 1
                            )
                            css_lines.extend(nested_lines)
                        else:
                            css_lines.append(f"{indentation}    {prop}: {value};")
                    
                    css_lines.append(f"{indentation}}}")
                
                return css_lines
            
            # Gera o CSS processado
            css_content = "\n".join(process_styles(self.styles, current_indent=indent))
            indentation = "    " * indent
            return f"{indentation}<style{' ' if len(self.kwargs) > 0 else ''}{' '.join(f'{key}=\"{value}\"' for key, value in self.kwargs.items())}>\n{css_content}\n{indentation}</style>"