from enum import Enum


class EventTriggerTypeEnum(str, Enum):
    MANUAL_CANCEL_SERVICE_TICKET = "manual_cancel_service_ticket"
    MANUAL_TRACING_START_SERVICE_TICKET = "manual_tracking_start_service_ticket"
    MANUAL_TRACING_STOP_SERVICE_TICKET = "manual_tracking_stop_service_ticket"
    MANUAL_CREATE_SERVICE_TICKET = "manual_create_service_ticket"
    MANUAL_IMPORT_RESERVATION_SMWS = "manual_import_reservation_smws"
    MANUAL_MODIFY_USER_SERVICE_TICKET = "manual_modify_user_service_ticket"
    MANUAL_MODIFY_ESTIMATED_ARRIVAL_TIME_SERVICE_TICKET = "manual_modify_estimated_arrival_time_service_ticket"
    MANUAL_MODIFY_ESTIMATED_DELIVERY_TIME_SERVICE_TICKET = "manual_modify_estimated_delivery_time_service_ticket"
    MANUAL_DELETE_ESTIMATED_DELIVERY_TIME_SERVICE_TICKET = "manual_delete_estimated_delivery_time_service_ticket"
    MANUAL_BOOKING_MESSAGE_SERVICE_TICKET = "manual_booking_message_service_ticket"
    MANUAL_DELIVERY_MESSAGE_SERVICE_TICKET = "manual_delivery_message_service_ticket"

    NOSHOW_SERVICE_TICKET_AUTO_CANCEL = "noshow_service_ticket_auto_cancel"
    IMPORT_RESERVATION_CONFLICT_AUTO_CANCEL = "import_reservation_conflict_auto_cancel"
    BOOKING_REMINDING_SERVICE_TICKET = "booking_reminding_service_ticket"
    TODAY_REPAIR_WORKING_SERVICE_TICKET_AUTO_CLOSED = "today_repair_working_service_ticket_auto_closed"

    LPNR_IN_ESTABLISHED = "lpnr_in_established"
    LPNR_IN_RECEPTION = "lpnr_in_reception"
    LPNR_IN_WORKING = "lpnr_in_working"
    LPNR_OUT = "lpnr_out"
    LPNR_OUT_GENERAL = "lpnr_out_general"
    LPNR_OUT_NO_SERVE = "lpnr_out_no_serve"
    LPNR_IN_POSITION = "lpnr_in_position"
    LPNR_OUT_POSITION = "lpnr_out_position"
