import pygame

class Keyboard:
    def __init__(self):
        """
        Makes it easier to take user input (via the keyboard)
        """
        self.keys = {
            pygame.K_a: "a",
            pygame.K_b: "b",
            pygame.K_c: "c",
            pygame.K_d: "d",
            pygame.K_e: "e",
            pygame.K_f: "f",
            pygame.K_g: "g",
            pygame.K_h: "h",
            pygame.K_i: "i",
            pygame.K_j: "j",
            pygame.K_k: "k",
            pygame.K_l: "l",
            pygame.K_m: "m",
            pygame.K_n: "n",
            pygame.K_o: "o",
            pygame.K_p: "p",
            pygame.K_q: "q",
            pygame.K_r: "r",
            pygame.K_s: "s",
            pygame.K_t: "t",
            pygame.K_u: "u",
            pygame.K_v: "v",
            pygame.K_w: "w",
            pygame.K_x: "x",
            pygame.K_y: "y",
            pygame.K_z: "z",
            pygame.K_0: "0",
            pygame.K_1: "1",
            pygame.K_2: "2",
            pygame.K_3: "3",
            pygame.K_4: "4",
            pygame.K_5: "5",
            pygame.K_6: "6",
            pygame.K_7: "7",
            pygame.K_8: "8",
            pygame.K_9: "9",
            pygame.K_TAB: "\t",
            pygame.K_SPACE: " ",
            pygame.K_SEMICOLON: ";",
            pygame.K_SLASH: "/",
            pygame.K_RETURN: "\n",
            pygame.K_PERIOD: ".",
            pygame.K_PLUS: "+",
            pygame.K_PERCENT: "%",
            pygame.K_MINUS: "-",
            pygame.K_HASH: "#",
            pygame.K_UNDERSCORE: "_",
            pygame.K_LEFTBRACKET: "(",
            pygame.K_RIGHTBRACKET: ")",
            pygame.K_LESS: "<",
            pygame.K_GREATER: ">",
            pygame.K_EQUALS: "=",
            pygame.K_EURO: "€",
            pygame.K_EXCLAIM: "!",
            pygame.K_QUESTION: "?",
            pygame.K_DOLLAR: "$",
            pygame.K_COLON: ":",
            pygame.K_COMMA: ",",
            pygame.K_BACKSLASH: "\\",
            pygame.K_ASTERISK: "*",
        }
        self.shift_keys = {
            pygame.K_a: "A",
            pygame.K_b: "B",
            pygame.K_c: "C",
            pygame.K_d: "D",
            pygame.K_e: "E",
            pygame.K_f: "F",
            pygame.K_g: "G",
            pygame.K_h: "H",
            pygame.K_i: "I",
            pygame.K_j: "J",
            pygame.K_k: "K",
            pygame.K_l: "L",
            pygame.K_m: "M",
            pygame.K_n: "N",
            pygame.K_o: "O",
            pygame.K_p: "P",
            pygame.K_q: "Q",
            pygame.K_r: "R",
            pygame.K_s: "S",
            pygame.K_t: "T",
            pygame.K_u: "U",
            pygame.K_v: "V",
            pygame.K_w: "W",
            pygame.K_x: "X",
            pygame.K_y: "Y",
            pygame.K_z: "Z",
            pygame.K_0: "=",
            pygame.K_1: "!",
            pygame.K_2: "\"",
            pygame.K_3: "§",
            pygame.K_4: "$",
            pygame.K_5: "%",
            pygame.K_6: "&",
            pygame.K_7: "/",
            pygame.K_8: "(",
            pygame.K_9: ")",
            pygame.K_PERIOD: ":",
            pygame.K_PLUS: "*",
            pygame.K_MINUS: "_",
            pygame.K_HASH: "'",
            pygame.K_LESS: ">",
            pygame.K_COMMA: ";"
        }
        self.__forbidden_chars__ = []

    def set_custom_value(self, custom_values: dict):
        """
        Sets custom return values specified by <custom_values>.
        """
        assert type(custom_values) == dict
        for k, v in custom_values.items():
            self.keys[k] = v
            self.shift_keys[k] = v

    def set_forbidden_characters(self, characters: list):
        """
        Bans all given characters.
        """
        assert type(characters) == list, f"invalid argument for 'characters': {characters}"
        for char in characters:
            assert type(char) == str, f"invalid character '{char}'"
            assert len(char) == 1, f"invalid character '{char}'"
            if char not in self.__forbidden_chars__:
                self.__forbidden_chars__.append(char)

    def get(self, event_list):
        """
        Returns a string of all keys pressed.
        """
        string = ""
        keys = pygame.key.get_pressed()
        # if keys[pygame.locals.K_LSHIFT] or keys[pygame.locals.K_RSHIFT]:
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            for e in event_list:
                if e.type == pygame.KEYDOWN and e.key:
                    char = self.shift_keys.get(e.key, "")
                    if char not in self.__forbidden_chars__:
                        string += char
        else:
            for e in event_list:
                if e.type == pygame.KEYDOWN and e.key:
                    char = self.keys.get(e.key, "")
                    if char not in self.__forbidden_chars__:
                        string += char
        return string
