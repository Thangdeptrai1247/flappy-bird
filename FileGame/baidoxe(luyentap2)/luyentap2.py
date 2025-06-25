import time
from abc import ABC, abstractmethod
#ticket
class Ticket():
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.entry_time = time.time()
    def calculate_fee(self):
        exit_time=time.time()
        duration_time = (exit_time - self.entry_time)/3600
        fee = duration_time * self.vehicle.get_fee_per_hour()
        return round(fee, 2)

#lớp cha trừu tượng
class Vehicle(ABC):
    def __init__(self,license_plate):
        self.license_plate = license_plate
    @abstractmethod
    def get_fee_per_hour(self):
        pass
#lớp con kế thừa từ lớp cha
class Car(Vehicle):
    def get_fee_per_hour(self):
        return 5
class Motorbike(Vehicle):
    def get_fee_per_hour(self):
        return 2
#Đỗ xe
class ParkingLot:
    def __init__(self, capacity):
        self.capacity = capacity
        self.tickets = {}
    def park_vehicle(self, vehicle):
        if len(self.tickets) >= self.capacity:
            print("Bãi đổ xe đã đầy")
            return
        if vehicle.license_plate in self.tickets:
            print('Xe đã có trong bãi')
            return
        ticket = Ticket(vehicle)
        self.tickets[vehicle.license_plate] = ticket
        print(f'xe{vehicle.license_plate} đã vào bãi')
    def remove_vehicle (self, license_plate):
        if license_plate not in self.tickets:
            print('Không tìm thấy bãi')
            return
        ticket = self.tickets.pop(license_plate)
        fee = ticket.calculate_fee()
        print(f'Xe{license_plate} đã rời khỏi bãi, phí gửi xe: {fee} USD')
    def show_vehicles(self):
        if not self.tickets:
            print('Bãi đổ xe còn trống')
        else:
            print('Các xe đang đỗ')
            for plate in self.tickets:
                print(f'-{plate}')

def show_menu():
    print('----------MENU---------')
    print('1.Đỗ xe')
    print('2.Rời bãi')
    print('3.Danh sách xe đang đỗ')
    print('4.Thoát')


def main():
    try:    
        capacity = int(input('Vui lòng chấp hành nội quy khi đi vào(nhập bấy kỳ số gì bạn muốn coi như là xác nhận)'))
    except ValueError:
        print('2Sức chứa phải là một số nguy')
        return
    parking_lot = ParkingLot(capacity)
    while True:
        show_menu()
        choice = input('Nhập lựa chọn của bạn').strip()

        if choice == '1':
            license_plate = input('Vui lòng nhập biển số xe một cách cẩn thận.').strip()
            vehicle_type = input('Phương tiện: Car/Motorbike').strip().lower()

            if vehicle_type == 'car':
                vehicle = Car(license_plate)
            elif vehicle_type == 'motorbike':
                vehicle = Motorbike(license_plate)
            else:
                print('Loại xe không hợp lệ')
                continue
        elif choice == '2':
            license_plate = input('Vui lòng nhập biển số xe rời bãi một cách cẩn thận để chúng tôi xác nhận xe bạn đã vào đây').strip()
            parking_lot.remove_vehicle(license_plate)
        elif choice == '3':
            parking_lot.show_vehicles()
        elif choice == '4':
            print('Chúc bạn thộ lộ bình an')
            break
        else:
            print('Lựa chọn không hợp lệ, vui lòng chọn lại')
        input('\n Nhấn enter để trở lại menu')
if __name__ == '__main__':
    main()
