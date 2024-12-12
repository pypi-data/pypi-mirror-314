from imxIcons.domain.atbvvInstallation.atbvvBeacon_v124 import (
    atbvv_beacon_entities_v124,
)
from imxIcons.domain.atbvvInstallation.atbvvBeacon_v500 import (
    atbvv_beacon_entities_v500,
)
from imxIcons.domain.axleCounterDetection.axleCounterDetectionPoint_v124 import (
    axle_counter_points_icon_entities_v124,
)
from imxIcons.domain.axleCounterDetection.axleCounterDetectionPoint_v500 import (
    axle_counter_points_icon_entities_v500,
)
from imxIcons.domain.departureSignal.departureSignal_imx500 import (
    departure_signal_entities_imx500,
)
from imxIcons.domain.insulatedJoint.insulatedJoint_v124 import (
    insulated_joint_entities_v124,
)
from imxIcons.domain.insulatedJoint.insulatedJoint_v500 import (
    insulated_joint_entities_v500,
)
from imxIcons.domain.levelCrossing.levelCrossing_v124 import (
    level_crossing_entities_v124,
)
from imxIcons.domain.levelCrossing.levelCrossing_v500 import (
    level_crossing_entities_v500,
)
from imxIcons.domain.sign.sign_imx124 import sign_icon_entities_v124
from imxIcons.domain.sign.sign_imx500 import sign_icon_entities_v500
from imxIcons.domain.signal.illuminated_signal_v124 import (
    illuminated_sign_icon_entities_v124,
)
from imxIcons.domain.signal.illuminated_signal_v500 import (
    illuminated_sign_icon_entities_v500,
)
from imxIcons.domain.signal.reflector_signal_v124 import (
    reflector_post_icon_entities_v124,
)
from imxIcons.domain.signal.reflector_signal_v500 import (
    reflector_post_icon_entities_v500,
)
from imxIcons.domain.signal.signal_imx124 import signals_icon_entities_v124
from imxIcons.domain.signal.signal_imx500 import signals_icon_entities_v500
from imxIcons.domain.speedsign.speedsign_imx124 import speed_sign_icon_entities_v124
from imxIcons.domain.speedsign.speedsign_imx500 import speed_sign_icon_entities_v500
from imxIcons.domain.supportedImxVersions import ImxVersionEnum
from imxIcons.iconEntity import IconEntity

ICON_DICT: dict[str, dict[str, list[IconEntity]]] = {
    "DepartureSignal": {
        ImxVersionEnum.v124.name: [],  # DepartureSignal is a SignalType in v124
        ImxVersionEnum.v500.name: departure_signal_entities_imx500,
    },
    "Signal": {
        ImxVersionEnum.v124.name: signals_icon_entities_v124,
        ImxVersionEnum.v500.name: signals_icon_entities_v500,
    },
    "Signal.IlluminatedSign": {
        ImxVersionEnum.v124.name: illuminated_sign_icon_entities_v124,
        ImxVersionEnum.v500.name: illuminated_sign_icon_entities_v500,
    },
    "Signal.ReflectorPost": {
        ImxVersionEnum.v124.name: reflector_post_icon_entities_v124,
        ImxVersionEnum.v500.name: reflector_post_icon_entities_v500,
    },
    "SpeedSign": {
        ImxVersionEnum.v124.name: speed_sign_icon_entities_v124,
        ImxVersionEnum.v500.name: speed_sign_icon_entities_v500,
    },
    "Sign": {
        ImxVersionEnum.v124.name: sign_icon_entities_v124,
        ImxVersionEnum.v500.name: sign_icon_entities_v500,
    },
    "AxleCounterDetectionPoint": {
        ImxVersionEnum.v124.name: axle_counter_points_icon_entities_v124,
        ImxVersionEnum.v500.name: axle_counter_points_icon_entities_v500,
    },
    "LevelCrossing": {
        ImxVersionEnum.v124.name: level_crossing_entities_v124,
        ImxVersionEnum.v500.name: level_crossing_entities_v500,
    },
    "ATBVVInstallation.ATBVVBeacon": {
        ImxVersionEnum.v124.name: atbvv_beacon_entities_v124,
        ImxVersionEnum.v500.name: [],
    },
    "AtbVvInstallation.AtbVvBeacon": {
        ImxVersionEnum.v124.name: [],
        ImxVersionEnum.v500.name: atbvv_beacon_entities_v500,
    },
    "InsulatedJoint": {
        ImxVersionEnum.v124.name: insulated_joint_entities_v124,
        ImxVersionEnum.v500.name: insulated_joint_entities_v500,
    },
}


DEFAULT_ICONS: dict[str, IconEntity | None] = {
    "Signal": None,
    "Signal.IlluminatedSign": None,
    "Signal.ReflectorPost": None,
    "SpeedSign": None,
    "Sign": None,
}
