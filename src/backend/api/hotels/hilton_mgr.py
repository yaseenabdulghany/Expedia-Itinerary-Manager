from .hotel_common import Hotel, HotelRequest, HotelReservation
from .hilton_external import HiltonHotelAPI, HiltonRoom, HiltonCustomerInfo
from ..common.reservation import IReservationManager
from ..common.customer_info import CustomerInfo


class HiltonHotelManager(IReservationManager):
    def search(self, request: HotelRequest):
        # location, from_date, to_date, adults, children, needed_rooms
        hotels_external = HiltonHotelAPI.search_rooms(request.location, request.datetime_from,
                                       request.datetime_to, request.adults,
                                       request.children, request.num_rooms)

        # Convert from the API hotel format to a unified project format
        hotels = []
        for hotel_external in hotels_external:
            # pass self as the generating manager
            hotel = Hotel('Hilton', hotel_external.price_per_night, request, self)
            hotels.append(hotel)
        return hotels

    def reserve(self, reservation: HotelReservation):
        # convert from our unified project format to airlines API
        hotel = self._to_hilton_hotel_external(reservation.hotel)
        customers_info = self._to_hilton_customers_info_external(reservation.customers_info)
        return HiltonHotelAPI.reserve_room(hotel, customers_info)

    def cancel(self, reservation):
        return HiltonHotelAPI.cancel_room(reservation.confirmation_id)

    @staticmethod
    def _to_hilton_hotel_external(hotel: Hotel):
        return HiltonRoom(hotel.request.room_type, hotel.request.num_rooms, hotel.price_per_night,
                          hotel.request.datetime_from, hotel.request.datetime_to)

    @staticmethod
    def _to_hilton_customers_info_external(customers_info: list):
        result = []
        for customer in customers_info:
            customer: CustomerInfo = customer
            result.append(HiltonCustomerInfo(customer.name, customer.passport_id, customer.birthdate))
        return result
