from hpSPMPlusStudio.NMIImporter.Decarators import*
from hpSPMPlusStudio.RequestManager.NMIEndpoint import NMIEndpoint
from hpSPMPlusStudio.RequestManager.NMICommand import NMICommand
from hpSPMPlusStudio.NMIManager.Managers.Controllers.StatusController import StatusController
from hpSPMPlusStudio.NMIManager.Managers.Controllers.ScannedImagesController import ScannedImagesController
from hpSPMPlusStudio.NMIManager.Managers.Controllers.SystemReadingsController import SystemReadingsController
from hpSPMPlusStudio.NMIManager.Managers.Controllers.ScanController import ScanController
from hpSPMPlusStudio.NMIManager.Managers.Controllers.OptionsController import OptionsController
from hpSPMPlusStudio.NMIManager.Managers.Controllers.XYOffsetController import XYOffsetController

PREFIX = "APP"
BASE_COMMAND = "DeviceInformations"

@Singleton
class NMIDevice:
    def __init__(self,endpoint:NMIEndpoint) -> None:
        self.DeviceEndpoint = endpoint
        self._CreateControllers()

    def Get_DeviceInfo(self)->dict:
        command = NMICommand(self.DeviceEndpoint,PREFIX,BASE_COMMAND)
        return command.execute_get()
    
    def _CreateControllers(self):
        self.Status = StatusController(self.DeviceEndpoint)
        self.ScannedImages = ScannedImagesController(self.DeviceEndpoint)
        self.SystemReadings = SystemReadingsController(self.DeviceEndpoint)
        self.Scan = ScanController(self.DeviceEndpoint)
        self.Options = OptionsController(self.DeviceEndpoint)
        self.XYOffset = XYOffsetController(self.DeviceEndpoint)

    def STATUS(self)->StatusController:
        return self.Status
    
    def SCAN(self)->ScanController:
        return self.Scan
    
    def SCANNEDIMAGES(self)->ScannedImagesController:
        return self.ScannedImages

    def SYSTEMREADINGS(self)->SystemReadingsController:
        return self.SystemReadings
    
    def OPTIONS(self)->OptionsController:
        return self.Options

    def XYOFFSET(self)->XYOffsetController:
        return self.XYOffset