import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
## import cmasher as cmr

def log_nums(start, stop, nums):
    return np.logspace(np.log10(start), np.log10(stop), num = nums)

bins=15
met_bins = log_nums(0.0001, 0.03, bins)

def runLinPlots():
    xvals = []
    for i in range(bins):
        bns_merge = pd.read_hdf(f'BNS_mergers_{np.round(met_bins[i], 5)}.h5', key='merger_bpp')
        m_binaries = pd.read_hdf(f'BNS_mergers_{np.round(met_bins[i], 5)}.h5', key='mass_binaries')
        #print(m_binaries.values[0][0])
        xvals.append(len(bns_merge)/m_binaries.values[0][0])
        

    #for i in range(bins):
        #kick_info = pd.read_hdf(f'BNS_mergers_{np.round(met_bins[i], 5)}.h5', key='kick_info')
        #m_binaries = pd.read_hdf(f'BNS_mergers_{np.round(met_bins[i], 5)}.h5', key='mass_binaries')
        #print(kick_info.values)
        #xvals.append(len(bns_merge)/m_binaries.values[0][0])

    plt.plot(met_bins, xvals)
    plt.xlabel("Metallicities (Z)")
    plt.xscale("log")
    plt.ylabel("Binaries per solar mass")
    plt.yscale("log")
    plt.savefig("metVsMass.png")
    plt.clf()
#log both axes

colors = ["lightskyblue", "deepskyblue", "royalblue", "navy", "black"]

def runHistPlots():
    legend_handles = []
    legend_labels = []
    
    # Plot histograms in a loop
    for i, color in zip(range(0, bins, 3), colors):
        bns_merge = pd.read_hdf(f'BNS_mergers_{np.round(met_bins[i], 5)}.h5', key='merger_bpp')
        plt.hist(np.log10(bns_merge.tphys), color=color, histtype = 'step', label=f"Metallicity = {np.round(met_bins[i], 5)}")
        print("working...\n")
        # Collect handles and labels for legend
        legend_handles.append(plt.Rectangle((0, 0), 1, 1, fc=color))
        legend_labels.append(f"Metallicity = {np.round(met_bins[i], 5)}")

    # Plot consolidated legend outside the loop
    plt.legend(handles=legend_handles, labels=legend_labels, loc = "upper right", fontsize = "x-small")

    plt.yscale("log")
    plt.xlabel('merger time [Myr]')
    plt.ylabel('Frequency')
    plt.show()

    plt.savefig('metVsTime.png')
    plt.clf()

    kick1 = []
    k1ce = []
    k1stab = []
    kick2, k2ce, k2stab = [], [], []
    vsys, vsysce, vsystab = [], [], []

def sepStabCe(bpp, kick_info):
    #import pdb
    #pdb.set_trace()
    #bpp_ce = bpp1.groupby('bin_num').filter(lambda x: (x['evol_type'] == 3).any() and (x['evol_type'] == 7).any())
    bpprlo = bpp.loc[bpp["evol_type"].isin([3, 7])]
    bpp_ce = bpprlo.loc[bpprlo["evol_type"] == 7]
    print(f'bpp_ce = {bpp_ce.count()}\n')
    #bpp_stab = bpp1.groupby('bin_num').filter(lambda x: (x['evol_type'] == 3).any() and not (x['evol_type'] == 7).any())
    bpp_stab = bpprlo.loc[~bpprlo["bin_num"].isin(bpp_ce["bin_num"])]
    print(f'bpp_stab = {bpp_stab.count()}')
    kick_ce = kick_info[kick_info["bin_num"].isin(bpp_ce["bin_num"])]
    kick_stab = kick_info[kick_info["bin_num"].isin(bpp_stab["bin_num"])]
    return bpp_ce, bpp_stab, kick_ce, kick_stab

def findTooBig(bpp, kick_info):
    vals = kick_info.loc[kick_info.vsys_1_total.values > 10000]
    fbpp = bpp[bpp["bin_num"].isin(vals["bin_num"])]
    return fbpp

def findEsc(kick_info):
    esc = kick_info.loc[kick_info.vsys_1_total.values < kick_info.natal_kick.values]
    bound = kick_info.loc[~kick_info["bin_num"].isin(esc["bin_num"])]
    return esc, bound

def runScatPlots():
    for i, color in zip(range(1), colors):
        kick_info = pd.read_hdf(f'dat_kstar1_13_kstar2_13_SFstart_13700.0_SFduration_0.0_metallicity_{np.round(met_bins[i], 8)}.h5', key='kick_info')
        bpp = pd.read_hdf(f'dat_kstar1_13_kstar2_13_SFstart_13700.0_SFduration_0.0_metallicity_{np.round(met_bins[i], 8)}.h5', key='bpp')
        bpp_ce, bpp_stab, kick_ce, kick_stab = sepStabCe(bpp, kick_info)
        #plt.plot(kick_info.values[1,3])
        #plt.plot(kick_info.values[2,3])
        kick1s = kick_info.loc[kick_info.star == 1]
        kick1vals = kick1s.natal_kick.values

        kick2s = kick_info.loc[kick_info.star == 2]
        kick2vals = kick2s.natal_kick.values

        kick1ce = kick_ce.loc[kick_ce.star == 1]
        k1cev = kick1ce.natal_kick.values

        kick2ce = kick_ce.loc[kick_ce.star == 2]
        k2cev = kick2ce.natal_kick.values

        kick1stab = kick_stab.loc[kick_stab.star == 1]
        k1stabv = kick1stab.natal_kick.values

        kick2stab = kick_stab.loc[kick_stab.star == 2]
        k2stabv = kick2stab.natal_kick.values
        
        vsys = kick1s.vsys_1_total.values
        vsysce = kick1ce.vsys_1_total.values
        vsystab = kick1stab.vsys_1_total.values

        #Separate by escape/bound
        esc, bound = findEsc(kick_info)
        esc1 = esc.loc[esc.star == 1]
        bound1 = bound.loc[bound.star == 1]
        esc2 = esc.loc[esc.star == 2]
        bound2 = bound.loc[bound.star == 2]
        
        #Should be second kick separated by whether they escaped / were bound by first kick
        esc12 = kick2s.loc[kick2s["bin_num"].isin(esc1["bin_num"])]
        bound12 = kick2s.loc[kick2s["bin_num"].isin(bound1["bin_num"])]

        #Try to separate clusters from kick1 to see differences
        
        import pdb
        pdb.set_trace()
        #Try to separate clusters from kick2 to see differences
        cl1_k2 = kick2s.loc[kick2s.natal_kick.values < 100]
        cl2_k2 = kick2s.loc[(~kick2s["bin_num"].isin(cl1_k2["bin_num"])) & (kick2s.vsys_total_1.values < 100)]
        cl3_k2 = kick2s.loc[(~kick2s["bin_num"].isin(cl1_k2["bin_num"])) & (~kick2s["bin_num"].isin(cl2_k2["bin_num"]))]

        #Plot separated by escape
        """ plt.scatter(esc1.natal_kick.values, esc1.vsys_1_total.values, color = "lightskyblue", label = 'Escaped system')
        plt.scatter(bound1.natal_kick.values, bound1.vsys_1_total.values, color = "navy", label = 'Bound to system')
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Kick1 Magnitude (km/s)")
        plt.ylabel("Velocity of system (km/s)")
        plt.legend()
        plt.savefig(f"k1vtotEsc{np.round(met_bins[i], 5)}.png") #6
        plt.clf()

        plt.scatter(esc12.natal_kick.values, esc12.vsys_1_total.values, color = "lightskyblue", label = 'Escaped system')
        plt.scatter(bound12.natal_kick.values, bound12.vsys_1_total.values, color = "navy", label = 'Bound to system')
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Kick2 Magnitude (km/s)")
        plt.ylabel("Velocity of system (km/s)")
        plt.legend()
        plt.savefig(f"k2vtotEsc1{np.round(met_bins[i], 5)}.png") #6
        plt.clf() """




        #Common plots...
        """ plt.scatter(kick1vals, vsys, color = color, label = f"Metallicity = {np.round(met_bins[i], 5)}")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Kick1 Magnitude (km/s)")
        plt.ylabel("Velocity of system (km/s)")
        plt.legend()
        plt.savefig(f"k1vtot{np.round(met_bins[i], 5)}.png") #6
        plt.clf()

        plt.scatter(kick2vals, vsys, color = color, label = f"Metallicity = {np.round(met_bins[i], 5)}")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Kick2 Magnitude (km/s)")
        plt.ylabel("Velocity of system (km/s)")
        plt.legend()
        plt.savefig(f"k2vtot{np.round(met_bins[i], 5)}.png") #6
        plt.clf()

        plt.scatter(k1cev, vsysce, color = color, label = f"Metallicity = {np.round(met_bins[i], 5)}", alpha = 1)
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Kick1 Magnitude (km/s)")
        plt.ylabel("Velocity of system (km/s)")
        plt.legend()
        plt.savefig(f"k1vtotce{np.round(met_bins[i], 5)}.png") #6
        plt.clf()
        print("plotted k1ce v vtot\n")

        plt.scatter(k1stabv, vsystab, color = color, label = f"Metallicity = {np.round(met_bins[i], 5)}")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Kick1 Magnitude (km/s)")
        plt.ylabel("Velocity of system (km/s)")
        plt.savefig(f"k1vtotstab{np.round(met_bins[i], 5)}.png") #6
        plt.clf()

        plt.scatter(k2stabv, vsystab, color = color, label = f"Metallicity = {np.round(met_bins[i], 5)}")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Kick2 Magnitude (km/s)")
        plt.ylabel("Velocity of system (km/s)")
        plt.legend()
        plt.savefig(f"k2vtotstab{np.round(met_bins[i], 5)}.png") #6
        plt.clf() """
        

        #end
        """ plt.scatter(kick1vals, kick2vals, color = color, label = f"Metallicity = {np.round(met_bins[i], 5)}")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Kick1 Magnitude (km/s)")
        plt.ylabel("Kick2 Magnitude (km/s)")
        plt.legend()
        plt.savefig(f"k1vk2{np.round(met_bins[i], 5)}.png") #6
        plt.clf() """
        

        """ plt.scatter(k1cev, k2cev, color = color, label = f"Metallicity = {np.round(met_bins[i], 5)}")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Kick1 Common Envelope (km/s)")
        plt.ylabel("Kick2 Common Envelope (km/s)") """

        """ plt.scatter(k1stabv, k2stabv, color = color, label = f"Metallicity = {np.round(met_bins[i], 5)}")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Kick1 Magnitude Stable Mass Transfer (km/s)")
        plt.ylabel("Kick2 Magnitude Stable Mass Transfer (km/s)") """
        #print(k1cev)


        """ plt.scatter(k2cev, vsysce, color = color, label = f"Metallicity = {np.round(met_bins[i], 5)}")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Kick2 Magnitude (km/s)")
        plt.ylabel("Velocity of system (km/s)")
        plt.legend()
        plt.savefig(f"k2vtotce{np.round(met_bins[i], 5)}.png") #6
        plt.clf() """

        

        print("plotting kicks... \n")

    plt.legend()

    """ plt.savefig("k1vtot.png") #1 """
    """ plt.savefig("k1vk2.png") #2  """
    """ plt.savefig("k2vtot.png") #3 """
    """ plt.savefig("k1vk2ce.png") #4 """
    """ plt.savefig("k1vk2stab.png") #5 """
    """ plt.savefig("k1vtotce.png") #6 """
    """ plt.savefig("k1vtotstab.png") #7 """
    """ plt.savefig("k2vtotce.png") #8 """
    """ plt.savefig("k2vtotstab.png") #9 """

runScatPlots()

# plt.scatter(kick1, kick2)
# plt.xlabel("Kick1 Magnitude (km/s)")
# #plt.xscale("log")
# plt.ylabel("Kick2 Magnitude (km/s)")
# #plt.yscale("log")
# plt.savefig("k1vk2.png")
# plt.clf()

# plt.scatter(k1ce, k2ce)
# plt.xlabel("Kick1 Magnitude (km/s)")
# #plt.xscale("log")
# plt.ylabel("Kick2 Magnitude (km/s)")
# #plt.yscale("log")
# plt.savefig("k1vk2ce.png")
# plt.clf()

# plt.scatter(k1stab, k2stab)
# plt.xlabel("Kick1 Magnitude (km/s)")
# #plt.xscale("log")
# plt.ylabel("Kick2 Magnitude (km/s)")
# #plt.yscale("log")
# plt.savefig("k1vk2stab.png")
# plt.clf()

# plt.scatter(kick1, vsys)
# plt.xlabel("Kick1 Magnitude (km/s)")

# plt.ylabel("Velocity of system (km/s)")

# plt.savefig("k1vtot.png")
# plt.clf()

# plt.scatter(k1ce, vsysce)
# plt.xlabel("Kick1 Magnitude (km/s)")

# plt.ylabel("Velocity of system (km/s)")

# plt.savefig("k1vtotce.png")
# plt.clf()

# plt.scatter(k1stab, vsystab)
# plt.xlabel("Kick1 Magnitude (km/s)")

# plt.ylabel("Velocity of system (km/s)")

# plt.savefig("k1vtotstab.png")
# plt.clf()

# plt.scatter(kick2, vsys)
# plt.xlabel("Kick2 Magnitude (km/s)")

# plt.ylabel("Velocity of system (km/s)")

# plt.savefig("k2vtot.png")
# plt.clf()

# plt.scatter(k2ce, vsysce)
# plt.xlabel("Kick2 Magnitude (km/s)")

# plt.ylabel("Velocity of system (km/s)")

# plt.savefig("k2vtotce.png")
# plt.clf()

# plt.scatter(k2stab, vsystab)
# plt.xlabel("Kick2 Magnitude (km/s)")

# plt.ylabel("Velocity of system (km/s)")

# plt.savefig("k2vtotstab.png")
# plt.clf()
