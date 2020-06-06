# ************************************ GAME ************************************
SECTOR_SIZE = 36

# ************************************ CREATURES.PY ************************************

pacman_hitbox_path = "../../res/hitbox/pacman.png"
pacman_animations_paths = {"move_left":  ["../../res/animations/pacman/move_left/0.png",
                                          "../../res/animations/pacman/move_left/1.png",
                                          "../../res/animations/pacman/move_left/2.png",
                                          "../../res/animations/pacman/move_left/3.png"],
                           "move_up":    ["../../res/animations/pacman/move_up/0.png",
                                          "../../res/animations/pacman/move_up/1.png",
                                          "../../res/animations/pacman/move_up/2.png",
                                          "../../res/animations/pacman/move_up/3.png"],
                           "move_right": ["../../res/animations/pacman/move_right/0.png",
                                          "../../res/animations/pacman/move_right/1.png",
                                          "../../res/animations/pacman/move_right/2.png",
                                          "../../res/animations/pacman/move_right/3.png"],
                           "move_down":  ["../../res/animations/pacman/move_down/0.png",
                                          "../../res/animations/pacman/move_down/1.png",
                                          "../../res/animations/pacman/move_down/2.png",
                                          "../../res/animations/pacman/move_down/3.png"],
                           "dead":       ["../../res/animations/pacman/dead/0.png",
                                          "../../res/animations/pacman/dead/1.png",
                                          "../../res/animations/pacman/dead/2.png",
                                          "../../res/animations/pacman/dead/3.png"]}

pacman_mana = 0
pacman_score = 0
pacman_lives = 3
pinky_animations_paths = {"move_left":  ["../../res/animations/pinky/move_left/0.png",
                                        "../../res/animations/pinky/move_left/1.png",
                                        "../../res/animations/pinky/move_left/2.png",
                                        "../../res/animations/pinky/move_left/3.png"],
                         "move_up":    ["../../res/animations/pinky/move_up/0.png",
                                         "../../res/animations/pinky/move_up/1.png",
                                         "../../res/animations/pinky/move_up/2.png",
                                         "../../res/animations/pinky/move_up/3.png"],
                         "move_right": ["../../res/animations/pinky/move_right/0.png",
                                         "../../res/animations/pinky/move_right/1.png",
                                         "../../res/animations/pinky/move_right/2.png",
                                         "../../res/animations/pinky/move_right/3.png"],
                         "move_down":  ["../../res/animations/pinky/move_down/0.png",
                                         "../../res/animations/pinky/move_down/1.png",
                                         "../../res/animations/pinky/move_down/2.png",
                                         "../../res/animations/pinky/move_down/3.png"],
                         "dead":       ["../../res/animations/pinky/dead/0.png",
                                         "../../res/animations/pinky/dead/1.png",
                                         "../../res/animations/pinky/dead/2.png",
                                         "../../res/animations/pinky/dead/3.png"]}

ghost_hitbox_path = "../../res/hitbox/ghost.png"
ghost_is_chasing = True

directions = ('left', 'up', 'right', 'down')
forms = ('red', 'green', 'blue')