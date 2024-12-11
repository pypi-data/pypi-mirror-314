from zs_utils.api.fedex.base_api import FedexAPI


class FedexCreatePickup(FedexAPI):
    http_method = "POST"
    resource_method = "/pickup/v1/pickups"
    required_params = [
        "associatedAccountNumber",
        "originDetail",
        "carrierCode",
    ]
    allowed_params = [
        "associatedAccountNumberType",
        "totalWeight",
        "packageCount",
        "accountAddressOfRecord",
        "remarks",
        "countryRelationships",
        "pickupType",
        "trackingNumber",
        "commodityDescription",
        "expressFreightDetail",
        "oversizePackageCount",
        "pickupNotificationDetail",
    ]


class FedexCheckPickupAvailability(FedexAPI):
    http_method = "POST"
    resource_method = "/pickup/v1/pickups/availabilities"
    required_params = [
        "pickupAddress",
        "pickupRequestType",
        "carriers",
        "countryRelationship",
    ]
    allowed_params = [
        "dispatchDate",
        "packageReadyTime",
        "customerCloseTime",
        "pickupType",
        "shipmentAttributes",
        "numberOfBusinessDays",
        "packageDetails",
        "associatedAccountNumber",
        "associatedAccountNumberType",
    ]


class FedexCancelPickup(FedexAPI):
    http_method = "PUT"
    resource_method = "/pickup/v1/pickups/cancel"
    required_params = [
        "associatedAccountNumber",
        "pickupConfirmationCode",
        "scheduledDate",
    ]
    allowed_params = [
        "remarks",
        "carrierCode",
        "accountAddressOfRecord",
        "location",
    ]
