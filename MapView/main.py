import asyncio
from kivy.app import App
from kivy_garden.mapview import MapMarker, MapView
from kivy.clock import Clock
from lineMapLayer import LineMapLayer
from datasource import Datasource
import csv
from functools import partial


class MapViewApp(App):
    def __init__(self, **kwargs):
        super().__init__()       
        self.line_map_layer = LineMapLayer()
        self.car_marker = MapMarker(source = "images/car.png")
        self.DS = Datasource(user_id = 1)
        # додати необхідні змінні


    def on_start(self):               
        self.mapview.add_layer(self.line_map_layer, mode="scatter")
        Clock.schedule_interval(self.update, 0.5)
        """
        Встановлює необхідні маркери, викликає функцію для оновлення мапи
        """

    def update(self, *args):
        new_points = self.DS.get_new_points()
        if len(new_points) != 0 :
            for point in new_points :
                point_location = [point[0], point[1]]
                self.update_car_marker(point_location)
                self.line_map_layer.add_point(point_location)
        """
        Викликається регулярно для оновлення мапи
        """

    def update_car_marker(self, point):
        self.mapview.remove_marker(self.car_marker)
        self.car_marker.lat = point[0]
        self.car_marker.lon = point[1]
        self.mapview.add_marker(self.car_marker)
        """
        Оновлює відображення маркера машини на мапі
        :param point: GPS координати
        """

    def set_pothole_marker(self, point):
        """
        Встановлює маркер для ями
        :param point: GPS координати
        """

    def set_bump_marker(self, point):
        """
        Встановлює маркер для лежачого поліцейського
        :param point: GPS координати
        """

    def build(self):
        """
        Ініціалізує мапу MapView(zoom, lat, lon)
        :return: мапу
        """
        self.mapview = MapView(zoom=15, lat = 0, lon = 0)
        return self.mapview


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(MapViewApp().async_run(async_lib="asyncio"))
    loop.close()
