from datetime import datetime
from typing import List

import numpy as np
import pydicom
from pydicom.dataset import Dataset
from pyPhases.util.Logger import classLogger
from pyPhasesRecordloader import Event, Signal

from SleepHarmonizer.recordwriter.RecordWriter import RecordWriter


@classLogger
class RecordWriterDICOM(RecordWriter):
    def getFilePath(self, recordName):
        return f"{self.filePath}/{recordName}.dcm"
    
    def writeSignals(self, recordName, channels: List[Signal], events: List[Event] = None, startTime: datetime = None, signalIsDigital=False):
        
        if events is None:
            events = []

        filePath = self.getFilePath(recordName)

        # if self.patient is not None:
        #     writer.setPatientName(self.patient.name)
        #     writer.setGender(self.patient.gender)

        psg = Dataset()

        psg.SOPClassUID =  "1.2.840.10008.5.1.4.1.1.9.1.2" # General ECG Waveform Storage
        psg.SOPInstanceUID = pydicom.uid.generate_uid()
            
        psg.WaveformSequence = []

        for index, channel in enumerate(channels):
            waveFormSequence = Dataset()
            waveFormSequence.MultiplexGroupLabel = channel.name
            waveFormSequence.MultiplexGroupTimeOffset = 0
            
            waveFormSequence.WaveformOriginality = "ORIGINAL"
            waveFormSequence.NumberOfWaveformChannels = 1
            waveFormSequence.NumberOfWaveformSamples = len(channel.signal)
            waveFormSequence.SamplingFrequency = channel.frequency

            sourceSequence = Dataset()
            sourceSequence.CodeValue = "1.0"
            sourceSequence.CodingSchemeDesignator = "PYDICOM"
            sourceSequence.CodingSchemeVersion = "1.0"
            sourceSequence.CodeMeaning = channel.name
            waveFormSequence.ChannelSourceSequence = [sourceSequence]


            diff = channel.digitalMax-channel.digitalMin
            requiredBits = np.ceil(np.log2(diff))

            digitalCenterDiff = (channel.digitalMax - channel.digitalMin + 1) / 2 + channel.digitalMin
            
            if requiredBits <= 8:
                sampleint = "SB"
                bits = 8
            elif requiredBits <= 16:
                sampleint = "SS"
                bits = 16
            elif requiredBits <= 32:
                sampleint = "SL"
                bits = 32
            else:
                sampleint = "SV"
                bits = 64

            digialToPhysical = ((channel.physicalMax - channel.physicalMin) / (channel.digitalMax - channel.digitalMin))
            baseLine = (channel.physicalMax + channel.physicalMin) / 2 + digitalCenterDiff*digialToPhysical

            channelDefinition = Dataset()
            channelDefinition.ChannelLabel = channel.name


            senssettings = Dataset()
            senssettings.CodeMeaning = ""
            senssettings.CodeValue = channel.dimension
            # senssettings.Label = channel.type.name
            channelDefinition.ChannelSensitivityUnitsSequence = [senssettings]

            channelDefinition.ChannelSensitivity = digialToPhysical
            channelDefinition.ChannelBaseline = baseLine
            channelDefinition.ChannelSampleSkew = 0
            channelDefinition.ChannelSensitivityCorrectionFactor = 1

            # channelDefinition.WaveformPaddingValue = 200
            # channelDefinition.FilterHighFrequency = 300
            # channelDefinition.FilterLowFrequency = 0.05
            # channelDefinition.NotchFilterFrequency = 0

            channelDefinition.WaveformBitsStored = bits
            
            waveFormSequence.ChannelDefinitionSequence = [channelDefinition]

            waveFormSequence.WaveformBitsAllocated = bits
            waveFormSequence.WaveformSampleInterpretation = sampleint
            waveFormSequence.WaveformData = (channel.signal - digitalCenterDiff).astype(f"int{bits}").reshape(-1, 1).tobytes()
            psg.WaveformSequence.append(waveFormSequence)

        psg.WaveformAnnotationSequence = []

        for event in events:
            waveFormAnnotation = Dataset()
            waveFormAnnotation.ReferencedWaveformChannels = [0]
            waveFormAnnotation.TemporalRangeType = "SEGMENT"
            waveFormAnnotation.ReferencedTimeOffsets = [event["start"], event["end"]]
            waveFormAnnotation.UnformattedTextValue = event["name"]
            psg.WaveformAnnotationSequence.append(waveFormAnnotation)

        psg.is_little_endian = True
        psg.is_implicit_VR = True
        psg.save_as(filePath, write_like_original=False)