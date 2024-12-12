from PySide6.QtWidgets import QPushButton

class PlayPushButton(QPushButton):

    def __init__(self, parent):
        super().__init__(parent)
        self.stop()
    
    def play(self, text="Play"):
        self.setStyleSheet(self._style_play())
        self.setText(text)
    
    def pause(self, text="Pause"):
        self.setStyleSheet(self._style_pause())
        self.setText(text)

    def stop(self, text="Stopp"):
        self.setStyleSheet(self._style_stop())
        self.setText(text)

    
    def _style_play(self, img_path='/icons/icons/cil-media-play.png'):
        return """
                /*Play Button*/
                QPushButton {		
                    background-position: left center;
                    background-repeat: no-repeat;
                    border: none;
                    border-radius: 0px;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: rgb(47, 104, 57);
                }
                QPushButton:pressed {	
                    background-color: rgb(44, 134, 46);
                    color: rgb(255, 255, 255);
                }
                QPushButton:disabled {	
                    background-color: rgb(153, 153, 153);
                    color: rgb(255, 255, 255);
                }
                """

    def _style_pause(selfm, img_path = "/icons/icons/cil-media-pause.png"):
        return """
            QPushButton {		
               background-color: rgb(255, 200,11);
                background-position: left center;
                background-repeat: no-repeat;
                border: none;
                border-radius: 0px;
                border-left: 22px solid transparent;
                text-align: left;
                padding-left: 44px;
                background-image: url(:""" + img_path + """)
            }
    
            QPushButton:hover {
                background-color: rgb(255, 182, 44);
            }
    
            QPushButton:pressed {	
                background-color: rgb(255, 146, 12);
                color: rgb(255, 255, 255);
            }
    
            QPushButton:disabled {	
                background-color: rgb(153, 153, 153);
                color: rgb(255, 255, 255);
            }
        """

    def _style_stop(self, img_path = "/icons/icons/cil-media-stop.png"):
        return """
            QPushButton {		
                background-color: rgb(242, 41, 41);
                background-position: left center;
                background-repeat: no-repeat;
                border: none;
                border-radius: 0px;
                border-left: 22px solid transparent;
                text-align: left;
                padding-left: 44px;
                background-image: url(:""" + img_path + """)
            }
            
            QPushButton:hover {
                background-color: rgb(235, 64, 52);
            }
            
            QPushButton:pressed {	
                background-color: rgb(201, 17, 4);
                color: rgb(255, 255, 255);
            }
            
            QPushButton:disabled {	
                background-color: rgb(153, 153, 153);
                color: rgb(255, 255, 255);
            }
        """
