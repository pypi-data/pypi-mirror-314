from hpSPMPlusStudio import NMICommand,NMIEndpoint,NMIDevice

if __name__ == "__main__":

    Endpoint = NMIEndpoint("192.168.10.53",9024)
    Device = NMIDevice(Endpoint)
    
    print(Device.Get_DeviceInfo())
    #print(Device.Status.Get_Commands())
    #print(Device.Status.Get_DashboardStatus())

    #print(Device.SystemReadings.Get_SystemReadings())
    #print(Device.SystemReadings.Get_SystemReadingsUnitText())
    print(Device.Scan.Get_Commands())

    print(Device.Scan.Get_XOffset())
    print(Device.Scan.Get_YOffset())
    print(Device.Scan.Get_ScanWidthPixel())
    print(Device.Scan.Get_ScanHeightPixel())
    print(Device.Scan.Get_ImageWidth())
    print(Device.Scan.Get_ImageHeight())
    print(Device.Scan.Get_IsImageSquare())
    print(Device.Scan.Get_ScanAngle())
    print(Device.Scan.Get_ScanSpeed())
    print(Device.Scan.Get_ScanNumberOfAverages())
    print(Device.Scan.Get_NumberOfScans())
    print(Device.Scan.Get_OffsetPosition())
    print(Device.Scan.Get_ScanDirection())
    print(Device.Scan.Get_IsRoundtripScan())
    print(Device.Scan.Get_IsSaveScannedImages())

    print(Device.XYOffset.Get_Commands())

    #print(Device.Options.Set_XYScale("pm"))
    #print(Device.Options.Set_ZScale("μm"))


    
    #print(Device.Status.Get_Status())
    #print(Device.ScannedImages.Get_NmiContainers())
    #print(Device.ScannedImages.Get_SelectedContainerImageList("tt"))
    #print(Device.ScannedImages.Get_SelectedContainerBackwardImageList("tt"))
    #print(Device.ScannedImages.Get_SelectedContainerForwardImageList("tt"))
    #print(Device.ScannedImages.Get_SelectedContainerImage("tt","ff"))