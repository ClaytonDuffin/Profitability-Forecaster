import numpy as np
import pandas as pd
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.cm as ColorMappable
from matplotlib import colors
import math
import warnings
warnings.filterwarnings("ignore")

commissionRate = 0.3 # what is kept per cost of item
processingRate = 0.029 # credit rate
processingSurcharge = 0.30 # transaction fee
maxConsultEstimate = 10 # max time per item in minutes
maxCostEstimate = 41 # maximum item cost
sharedRate = 0.25 # what the employees keep of revenue
inboundVoiceLeg = 0.022 # price for incoming phone calls (excluding IVR)
outboundVoiceLeg = 0.013 # price for outgoing phone calls (excluding IVR)
outboundToInbound = 0.84 # proportion of outbound to inbound calls for voice
blendedLegs = (outboundToInbound * outboundVoiceLeg) + ((1 - outboundToInbound) * inboundVoiceLeg) # outbound and inbound voice costs combined
IVRminutes = 2 # minutes spent on the phone with <pay> IVR per transaction
tollFreeIVROutboundLeg = 0.0220 # <pay> IVR costs per minute
IVRCost = tollFreeIVROutboundLeg * IVRminutes # <pay> IVR total costs
smsOutgoing = 0.0079 # outgoing SMS cost per text
smsIncoming = 0.0079 # incoming SMS cost per text
smsFactor = 35 # number of texts estimated to be sent per transaction
smsIncomingFactored = ((1 / smsFactor) * smsIncoming) # price per transaction for incoming SMS
smsCosts = (smsOutgoing * smsFactor) + smsIncomingFactored # total SMS costs per transaction
emailDomainExpenses = 1.67 # monthly expense
cloudHostingExpenses = 0.0 # monthly expense
websiteExpenses = 2.59 # monthly expense
callForwardingExpenses = 0.0 # monthly expense
miscExpenses = 5.39 # in dollars for period
monthlyPhoneNumber = 1.15 # monthly expense

numberOfItems, costPerItem, parameterSet, timePerConsultParameter, costsPerItem, profitPerScenario, itemNumbers, expensesPerIteration = [], [], [], [], [], [], [], []

for price in range(0, maxCostEstimate, 1): 
    costPerItem.append(price)
    
for items in range(1, 25, 1):
    numberOfItems.append(items)
    
for a in costPerItem:
    
    for b in numberOfItems:
        
        grossDollarVolume = a * b
        revenue = grossDollarVolume * commissionRate
        
        callExpenses = ((maxConsultEstimate * blendedLegs) + IVRCost) * b
        smsExpenses = (b * smsCosts)
        
        inboundCreditSurcharge = ((b * processingSurcharge))
        inboundCreditRateExpenses = (((grossDollarVolume) + (grossDollarVolume * (commissionRate / 2))) * processingRate)
        outboundCreditRateExpenses = (((grossDollarVolume) - (grossDollarVolume * (commissionRate / 2))) * processingRate)
        
        employeePayroll = (revenue * sharedRate)
        variableExpenses = (callExpenses + smsExpenses + inboundCreditSurcharge + inboundCreditRateExpenses + outboundCreditRateExpenses)
        fixedExpenses = (emailDomainExpenses + cloudHostingExpenses + websiteExpenses + callForwardingExpenses + monthlyPhoneNumber  + miscExpenses)
        
        netProfit = revenue - (employeePayroll + fixedExpenses + variableExpenses)
        
        costsPerItem.append(a)
        itemNumbers.append(b)
        expensesPerIteration.append(variableExpenses + fixedExpenses)
        profitPerScenario.append(netProfit)


profitForEachScenario = pd.DataFrame(profitPerScenario)
print('\nProfit for Period: $' + str(round(profitForEachScenario.mean()[0], 2)))
print('\nFixed to Variable Expense Ratio: ' + str(round((fixedExpenses / variableExpenses), 4)))
print('\nEfficiency Ratio: ' + str(round(((sum(expensesPerIteration) / len(expensesPerIteration)) / ((sum(expensesPerIteration) / len(expensesPerIteration)) + float(profitForEachScenario.mean()))), 4))) # plot efficiency ratio as function of number of items to illustrate breakeven at 1.00 and asymptotic behavior.

fig, ax1 = plt.figure(), plt.subplot(projection = '3d')

ensuringCorrectColorScales = ColorMappable.ScalarMappable(cmap = ColorMappable.seismic) 
ensuringCorrectColorScales.set_array(np.asarray(profitForEachScenario)) 
colorScheme = colors.TwoSlopeNorm(vmin = -(math.floor(profitForEachScenario.max())), vcenter = 0, vmax = math.floor(profitForEachScenario.max())) 
colorMap = plt.get_cmap('seismic') 
ensuringCorrectColorScales.set_clim((math.floor(profitForEachScenario.max())), -(math.floor(profitForEachScenario.max())))

ax1.plot_trisurf(np.asarray(itemNumbers),
                 np.asarray(costsPerItem),
                 np.asarray(profitPerScenario),
                 antialiased = False,
                 cmap = colorMap,
                 norm = colorScheme)

ax1.set_title('Shared Profit \n Compensation Structure', x = 0.35, y = 0.94)
ax1.set_xlabel('Number of Items')
ax1.set_ylabel('Cost per Item')
ax1.set_zlabel('Net Profit', labelpad = 7)
ax1.azim = -80
ax1.dist = 11
ax1.elev = 15
plt.colorbar(ensuringCorrectColorScales)
