from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking
from domain.aggregated_data import AggregatedData
import config



class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
        parking_filename: str,
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.accelerometer_data = []
        self.gps_data = []
        self.parking_data = []
        self.accelerometer_index = 0
        self.gps_index = 0
        self.parking_index = 0
        self.all_data_read = False  # Додано змінну для відстеження прочитаних даних


    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""
        with open(self.accelerometer_filename, 'r') as accelerometer_file:
            csv_reader = reader(accelerometer_file)
            next(csv_reader)
            self.accelerometer_data = list(csv_reader)

        with open(self.gps_filename, 'r') as gps_file:
            csv_reader = reader(gps_file)
            next(csv_reader)
            self.gps_data = list(csv_reader)

        with open(self.parking_filename, 'r') as parking_file:
            csv_reader = reader(parking_file)
            next(csv_reader)
            self.parking_data = list(csv_reader)


    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        if self.all_data_read:
            return None  # Якщо всі дані вже прочитані, повертаємо None

        if not self.accelerometer_data or not self.gps_data or not self.parking_data:
            return None  # Якщо дані закінчилися, повертаємо None

        accelerometer_row = self.accelerometer_data[self.accelerometer_index]
        gps_row = self.gps_data[self.gps_index]
        parking_row = self.parking_data[self.parking_index]

        accelerometer_data = list(map(float, accelerometer_row))
        gps_data = list(map(float, gps_row))
        parking_data = list(map(float, parking_row))
        print(parking_data)

        self.accelerometer_index = (self.accelerometer_index + 1) % len(self.accelerometer_data)
        self.gps_index = (self.gps_index + 1) % len(self.gps_data)
        self.parking_index = (self.parking_index + 1) % len(self.parking_data)

        self.stopReading()

        return AggregatedData(
            Accelerometer(*accelerometer_data),
            Gps(*gps_data),
            Parking(parking_data[0], Gps(parking_data[1], parking_data[2])),
            datetime.now(),
            config.USER_ID,
        )

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        if self.accelerometer_index == 0 and self.gps_index == 0 and self.parking_index == 0:
            self.all_data_read = True  # Позначаємо, що всі дані прочитані
