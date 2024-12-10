
V10_ELEMENT_CLASS:      str = 'GraphicClass'
V10_ELEMENT_FIELD:      str = 'Field'
V10_ELEMENT_METHOD:     str = 'Method'
V10_ELEMENT_PARAMETER:  str = 'Param'
V10_ELEMENT_INTERFACE2: str = 'Interface'
V10_ELEMENT_NOTE:       str = 'GraphicNote'
V10_ELEMENT_TEXT:       str = 'GraphicText'

V10_ELEMENT_LABEL_CENTER:      str = 'LabelCenter'
V10_ELEMENT_LABEL_SOURCE:      str = 'LabelSrc'
V10_ELEMENT_LABEL_DESTINATION: str = 'LabelDst'

V10_ATTR_ID:                 str = 'id'
V10_ATTR_NAME:               str = 'name'
V10_ATTR_TYPE:               str = 'type'
V10_ATTR_STEREOTYPE:         str = 'stereotype'
V10_ATTR_DEFAULT_VALUE:      str = 'defaultValue'

V10_ATTR_DISPLAY_STEREOTYPE: str = 'showStereotype'
V10_ATTR_DISPLAY_METHODS:    str = 'showMethods'
V10_ATTR_DISPLAY_FIELDS:     str = 'showFields'
V10_ATTR_DISPLAY_PARAMETERS: str = 'displayParameters'

V10_ATTR_CARDINALITY_SOURCE:      str = 'cardSrc'
V10_ATTR_CARDINALITY_DESTINATION: str = 'cardDestination'
V10_ATTR_BIDIRECTIONAL:           str = 'bidir'
V10_ATTR_SOURCE_ID:               str = 'sourceId'
V10_ATTR_DESTINATION_ID:          str = 'destId'
V10_ATTR_SOURCE_TIME:             str = 'srcTime'
V10_ATTR_DESTINATION_TIME:        str = 'dstTime'

V10_ATTR_SD_MESSAGE_SOURCE_ID:       str = 'srcID'
V10_ATTR_SD_MESSAGE_DESTINATION_ID:  str = 'dstID'

V10_ATTR_FILENAME: str = 'filename'

V11_ELEMENT_CLASS:      str = 'OglClass'
V11_ELEMENT_FIELD:      str = 'PyutField'
V11_ELEMENT_METHOD:     str = 'PyutMethod'
V11_ELEMENT_PARAMETER:  str = 'PyutParameter'
V11_ELEMENT_INTERFACE2: str = 'PyutInterface'
V11_ELEMENT_NOTE:       str = 'OglNote'
V11_ELEMENT_TEXT:       str = 'OglText'


V11_ATTR_STEREOTYPE:             str = 'stereotype'
V11_ATTR_DISPLAY_STEREOTYPE:     str = 'displayStereotype'
V11_ATTR_DISPLAY_METHODS:        str = 'displayMethods'
V11_ATTR_DISPLAY_FIELDS:         str = 'displayFields'
V11_ATTR_DISPLAY_PARAMETERS:     str = 'displayParameters'
V11_ATTR_DISPLAY_CONSTRUCTOR:    str = 'displayConstructor'
V11_ATTR_DISPLAY_DUNDER_METHODS: str = 'displayDunderMethods'

V11_ATTR_ID:                 str = V10_ATTR_ID
V11_ATTR_NAME:               str = 'name'
V11_ATTR_TYPE:               str = 'type'
V11_ATTR_DEFAULT_VALUE:      str = 'defaultValue'

V11_ATTR_CARDINALITY_SOURCE:      str = 'cardinalitySource'
V11_ATTR_CARDINALITY_DESTINATION: str = 'cardinalityDestination'
V11_ATTR_BIDIRECTIONAL:           str = 'bidirectional'
V11_ATTR_SOURCE_ID:               str = 'sourceId'
V11_ATTR_DESTINATION_ID:          str = 'destinationId'
V11_ATTR_SOURCE_TIME:             str = 'sourceTime'
V11_ATTR_DESTINATION_TIME:        str = 'destinationTime'

V11_ATTR_SD_MESSAGE_SOURCE_ID:       str = V11_ATTR_SOURCE_ID
V11_ATTR_SD_MESSAGE_DESTINATION_ID:  str = V11_ATTR_DESTINATION_ID

V11_ATTR_FILENAME: str = 'fileName'

#
# Use Case Diagrams
#

V10_ELEMENT_ACTOR:    str = 'GraphicActor'
V10_ELEMENT_USE_CASE: str = 'GraphicUseCase'
V10_ELEMENT_INSTANCE: str = 'GraphicSDInstance'
V10_ELEMENT_MESSAGE:  str = 'GraphicSDMessage'

V11_ELEMENT_ACTOR:    str = 'OglActor'
V11_ELEMENT_USE_CASE: str = 'OglUseCase'
V11_ELEMENT_INSTANCE: str = 'OglSDInstance'
V11_ELEMENT_MESSAGE:  str = 'OglSDMessage'
#
# Links
#
V10_ELEMENT_OGL_LINK:       str = 'GraphicLink'
V10_ELEMENT_OGL_INTERFACE2: str = 'GraphicLollipop'

V11_ELEMENT_LABEL_CENTER:      str = 'LabelCenter'
V11_ELEMENT_LABEL_SOURCE:      str = 'LabelSource'
V11_ELEMENT_LABEL_DESTINATION: str = 'LabelDestination'

V10_ELEMENT_LINK:           str = 'Link'

V11_ELEMENT_OGL_LINK:       str = 'OglLink'
V11_ELEMENT_OGL_INTERFACE2: str = 'OglInterface2'
V11_ELEMENT_LINK:           str = 'PyutLink'
