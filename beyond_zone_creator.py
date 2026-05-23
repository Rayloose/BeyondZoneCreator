number_zone = int(input("Enter the number of zones to create: "))
zone_initial_name = str(input("Enter the initial name for the zones: "))
print(
    "server mode : \n"
    "1 : no dmx adress\n"
    "2 : Classic FB3 style (16 DMX channels)\n"
    "3 : Mide-size profile (32 DMX channels)\n"
    "4 : Max-size profile (50 DMX channels)\n"
    "5 : FB4 style (39 DMX channels)\n"
)
server_mode = int(input("Enter the server mode (1-5): "))
max_dmx_address = int(input("Enter the maximum DMX address (usually 512): "))
fixtures_per_universe = int(input("Enter the number of fixtures per universe (for limited mode): "))
completion_mode = str(input("Enter completion mode (full or limited): "))

filename = f"{number_zone}_zone_server_{server_mode}.csv"

data_for_zone = [zone_initial_name, server_mode,number_zone]

dmx_channel_from_server_mode = {1:1 ,2:16, 3:32, 4:50, 5:39}


first_line = '"Zone Name",Projector,"Server Mode","DMX Universe","DMX Address","Vis Fixture"'

def create_csv_file(zone_data, file_name):
    with open(file_name, 'w') as f:
        f.write(first_line + '\n')
        for zone in zone_data:
            f.write(f'"{zone["name"]}",{zone["projector"]},{zone["server_mode"]},{zone["dmx_universe"]},{zone["dmx_address"]},{zone["vis_fixture"]}\n')

def set_zone_data(data_for_zone, completion_mode = "full"):

    zone_data = []
    dmx_universe = 1
    dmx_address = 1
    
    dmx_channel = dmx_channel_from_server_mode[server_mode]

    for i in range(data_for_zone[2]):
        
        if completion_mode == "full" : # we fill completely the dmx universe
            if max_dmx_address < dmx_address + dmx_channel - 1 :
                dmx_universe +=1
                dmx_address = 1
        elif completion_mode == "limited" : # we limit the number of fixtures per universe
            if i%fixtures_per_universe == 0 and i != 0 :
                dmx_universe +=1
                dmx_address = 1

        if data_for_zone[1] == 1 : # no dmx address
            dmx_address = 0
            dmx_universe = 0

        zone_data.append({
            "name" : data_for_zone[0] + f"{i+1}",
            "projector" : i+1,
            "server_mode" : data_for_zone[1],
            "dmx_universe" : dmx_universe,
            "dmx_address" : dmx_address,
            "vis_fixture" : i+1
        }
        )

        dmx_address += dmx_channel

    return zone_data

zone_data = set_zone_data(data_for_zone, completion_mode)
create_csv_file(zone_data, filename)

print(f"\nFichier '{filename}' créé avec succès avec {len(zone_data)} zones.")
print("Appuyez sur Entrée pour fermer le programme...")
input()



