# Notes: -script that uses the bom of an electric machine to calculate the environmental impact of its production
#        -details and references at https://ukconfluence01.romaxtech.com/confluence/display/RUB/Motor+LCA
# Changelog
# v1 created
# v2 added ferrite material

# variables description
# em_bom        -   electric machine bill of materials (input 1D array)
# em_pei        -   electric machine total production environmental impact matrix (output 2D array)
# em_pei_kg     -   electric machine materials per kg environmental impact matrix



# input variables
# 10x1 matrix
# em_bom matrix is an input as in the example below
# em_bom_row_header = ['Electrical steel', 'Other steel', 'Aluminum', 'Copper', 'Insulation materials',
#                      'Insulation resins', 'Paint', 'Plastics', 'NdFeB', 'Ferrite']
em_bom = [[107],[10],[16],[10],[0.5],[2],[1.5],[0.5],[2.5],[0]]


# 12x1 matrix
# em_pei_row_header = ['Climate change', 'Fossil depletion', 'Freshwater ecotoxicity', 'Freshwater eutrophication',
#                      'Human toxicity', 'Ionising radiation', 'Metal depletion', 'Ozone depletion',
#                      'Particulate matter formation', 'Photochemical oxidant formation', 'Terrestrial acidification',
#                      'Terrestrial ecotoxicity']
em_pei_row_header_units = ["kg CO2", "kg oil", "kg 1.4-DCB", "kg P", "kg 1.4-DCB", "kg U235",
                           "kg Fe", "kg CFC-11", "kg PM10", "kg NMVOC", "kg SO2", "kg 1.4-DCB"]
em_pei = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]


# 12x10 matrix
em_pei_kg_row_header = ['Climate change', 'Fossil depletion', 'Freshwater ecotoxicity', 'Freshwater eutrophication',
                        'Human toxicity', 'Ionising radiation', 'Metal depletion', 'Ozone depletion',
                        'Particulate matter formation', 'Photochemical oxidant formation', 'Terrestrial acidification',
                        'Terrestrial ecotoxicity']
# em_pei_kg_column_header = ['Electrical steel', 'Other steel', 'Aluminum', 'Copper', 'Insulation materials',
#                            'Insulation resins', 'Paint', 'Plastics', 'NdFeB', 'Ferrite']

em_pei_kg = [
    [1.68E+00, 2.20E+00, 9.38E+00, 1.30E+00, 5.00E-01, 5.50E+00, 2.13E+00, 2.40E+00, 1.00E+01, 4.36E-01],
    [5.98E-01, 6.50E-01, 2.19E+00, 4.00E-01, 1.88E-01, 2.40E+00, 1.00E+00, 1.80E+00, 4.80E+00, 1.32E-01],
    [3.36E-02, 1.30E-01, 4.50E-02, 4.00E-02, 1.04E-03, 6.00E-03, 7.33E-03, 4.20E-03, 2.08E-01, 9.00E-03],
    [2.06E+00, 2.50E+00, 8.75E+00, 1.40E+00, 7.60E-01, 7.50E+00, 2.67E+00, 2.80E+00, 1.16E+01, 1.91E-01],
    [5.61E+00, 8.90E+00, 5.13E+01, 1.30E+02, 5.20E-01, 8.50E+00, 5.07E+00, 6.60E+00, 2.84E+01, 5.20E-01],
    [3.36E-01, 6.30E-01, 2.19E+00, 3.80E-01, 3.40E-02, 7.50E-01, 4.67E-01, 5.80E-01, 1.64E+00, 3.40E-02],
    [5.05E+00, 2.70E+00, 4.63E-01, 2.20E+01, 5.60E-03, 2.05E-01, 1.47E-01, 1.56E-01, 1.96E+00, 1.96E-01],
    [1.78E-07, 1.70E-07, 5.69E-07, 1.00E-07, 8.20E-09, 5.50E-07, 3.00E-07, 6.00E-07, 1.60E-06, 4.96E-09],
    [6.92E-03, 5.50E-02, 1.69E-02, 3.10E-02, 8.40E-04, 9.00E-03, 4.67E-03, 3.40E-03, 2.32E-02, 6.04E-04],
    [6.82E-03, 3.20E-02, 2.13E-02, 2.30E-02, 2.00E-03, 2.15E-02, 8.00E-03, 8.80E-03, 2.88E-02, 2.00E-03],
    [7.85E-03, 2.20E-01, 3.75E-02, 8.50E-02, 2.40E-03, 2.30E-02, 1.40E-02, 9.80E-03, 5.20E-02, 2.40E-03],
    [2.43E-03, 1.50E-02, 1.19E-02, 7.70E-02, 6.60E-05, 2.50E-03, 3.00E-03, 8.20E-04, 1.08E-02, 6.60E-05]
            ]



# em_pei = em_pei_kg x em_bom    multiplication of 12x9 and 9x1 matrices
for i in range(len(em_pei_kg)):
    for j in range (len(em_bom[0])):
        for k in range (len(em_bom)):
            em_pei[i][j] += em_pei_kg[i][k] * em_bom[k][j]


# print results
print("\n")
print("Impact category                   Value       Units")
for i in range(len(em_pei)):
    print(em_pei_kg_row_header[i],(32-len(em_pei_kg_row_header[i]))*".", "{:.3e}".format(em_pei[i][0]),'.',
          em_pei_row_header_units[i])

