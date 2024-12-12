from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QCoreApplication


class Animation(object):
    
    @classmethod
    def minimumWidth(cls, widget : QWidget, start_value : int, end_value : int , duration = 500, easing_curve_type = QEasingCurve.Type.InOutQuart):
        instance = QCoreApplication.instance().activeWindow()
        if instance:
            instance.animation = QPropertyAnimation(widget, b"minimumWidth")
            instance.animation.setDuration(duration)
            instance.animation.setStartValue(start_value)
            instance.animation.setEndValue(end_value)
            instance.animation.setEasingCurve(easing_curve_type)
            instance.animation.start()
        else:
            print('Animation: Active window not found')



