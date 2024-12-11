def test_test():
    assert 0==0

# import pickle
# import sys

# sys.path.append("./mly/")
# from mly.datatools       import DataPod
# from mly.null_energy_map import *

# config = dict(
#     nside    = 64,
#     fs       = 1024,
#     duration = 1 
# )

# with open(f"./test_buffers/T_1348224727.0_HLV_buffer.pkl", 'rb') as obj:
#     buffer = pickle.load(obj)
    
# # Create skymap plugin:
# sky_map_plugin = \
#     createSkymapPlugin(
#         config["nside"], 
#         config["fs"], 
#         config["duration"]
#     )

# # Generate skymap:
# buffer.addPlugIn(sky_map_plugin)

# buffer.plot(type_="null_energy_map")
# plt.savefig("skymap_test.png")

