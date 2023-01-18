import random
import lb_set_data_polygon as lb_set_data



# get drops reference dictionary and returns dropchance filled dictionary
# dropchance is considered over 10000 (eg. dropchance of 1500 is 15%)
def get_dropchance_filled_dict(ref_dict):
    filled_dict = {}
    for slot in ref_dict:
        denominator_proportional = sum([lb_set_data.drop_proportion[x[1]] for x in ref_dict[slot][1:]])
        none_drop = dict(ref_dict[slot])['none']
        base_drop = (10000-none_drop) / denominator_proportional if denominator_proportional != 0 else 0
        # list of (item, dropchance) for this slot
        filled_dict[slot] = []
        for style, rarity in ref_dict[slot]:
            dropchance = base_drop * lb_set_data.drop_proportion[rarity] if style != 'none' else none_drop
            filled_dict[slot].append((style, round(dropchance)))
    return filled_dict

boy_drops = get_dropchance_filled_dict(lb_set_data.boy_drops_ref)
girl_drops = get_dropchance_filled_dict(lb_set_data.girl_drops_ref)

# filter for wanted OR unwanted styles
def filter_drops(drops, wanted_styles=(), unwanted_styles=()):
    if (wanted_styles and unwanted_styles):
        raise ValueError('input wanted OR unwanted styles')
    if wanted_styles:
        return [d for d in drops if d[0].startswith(wanted_styles)]
    if unwanted_styles:
        return [d for d in drops if not d[0].startswith(unwanted_styles)]
    return []

# weighted random choice
def random_drop(drops):
    total_weight = sum([drop[1] for drop in drops])
    selected_weight = random.randint(1, total_weight)
    cumulative_weight = 0
    for drop in drops:
        cumulative_weight += drop[1]
        if cumulative_weight >= selected_weight:
            return drop[0]



# slot specific rules
def boy__get_hair_according_to_hat(hat):
    have_hat = hat != 'none'
    if have_hat:
        is_backcap = hat in ('style29', 'style30', 'style31', 'style32') # backcap hat styles: 29 30 31 32
        if is_backcap:
            backcap_hairs = filter_drops(boy_drops['hair'], wanted_styles=('style09',)) # backcap hair style: 09
            return random_drop(backcap_hairs)
        else:
            short_hairs = filter_drops(boy_drops['hair'], wanted_styles=('style01',)) # short hair style: 01
            return random_drop(short_hairs)
    nohat_hairs = filter_drops(boy_drops['hair'], unwanted_styles=('style09',))
    return random_drop(nohat_hairs)

def boy__get_beard_according_to_hair(hair):
    random_beard = random_drop(boy_drops['beard'])
    is_colored_beard = len(random_beard.split('_')) > 1
    is_colored_hair = len(hair.split('_')) > 1
    if is_colored_beard and is_colored_hair:
        beard_style = random_beard.split('_')[0]
        beard_color = random_beard.split('_')[1]
        hair_color = hair.split('_')[1]
        if beard_color != hair_color:
            new_beard = beard_style + '_' + hair_color
            if new_beard in [x[0] for x in boy_drops['beard']]:
                return new_beard
    return random_beard

def boy__get_legs_according_to_torso(torso):
    # onepiece torso styles: 34, 35, 36, 37, 38, 39, 40
    if torso in ('style34', 'style35', 'style36', 'style37', 'style38', 'style39', 'style40'):
        return 'none'
    else:
        return random_drop(boy_drops['legs'])

def boy__get_torso_according_to_jacket(jacket):
    if jacket != 'none':
        # shirt torso (no apron) styles: 02 - 22
        shirts_no_apron = filter_drops(boy_drops['torso'], wanted_styles=('style02', 'style03', 'style04', 'style05', 'style06', 'style07', 'style08', 'style09', 'style10', 'style11', 'style12', 'style13', 'style14', 'style15', 'style16', 'style17', 'style18', 'style19', 'style20', 'style21', 'style22'))
        return random_drop(shirts_no_apron)
    return random_drop(boy_drops['torso'])

# slot specific rules

def girl__get_hair_according_to_hat(hat):
    have_hat = hat != 'none'
    # headband hat styles: 29 30 31 32
    is_headband = hat in ('style29', 'style30', 'style31', 'style32') 
    if have_hat:
        if is_headband:
            headband_hairs = filter_drops(girl_drops['hair'], unwanted_styles=('style05',)) # sideshaved hair style: 05
            return random_drop(headband_hairs)
        else:
            hat_hairs = filter_drops(girl_drops['hair'], wanted_styles=('style01',)) # chanel hair style: 01
            return random_drop(hat_hairs)
    return random_drop(girl_drops['hair'])

def girl__get_torso_according_to_jacket(jacket):
    # shirts no apron styles 02-23
    shirts_no_apron = ('style02', 'style03', 'style04', 'style05', 'style06', 'style07', 'style08', 'style09', 'style10', 'style11', 'style12', 'style13', 'style14', 'style15', 'style16', 'style17', 'style18', 'style19', 'style20', 'style21', 'style22', 'style23')
    # dresses styles 32-44
    dresses = ('style32', 'style33', 'style34', 'style35', 'style36', 'style37', 'style38', 'style39', 'style40', 'style41', 'style42', 'style43', 'style44')
    # big jacket styles: 01 02 03 04 05
    is_bigjacket = jacket in ('style01', 'style02', 'style03', 'style04', 'style05')
    if is_bigjacket:
        shirts_no_apron_torsos = filter_drops(girl_drops['torso'], wanted_styles=shirts_no_apron)
        return random_drop(shirts_no_apron_torsos) ##
    # other jackets
    if jacket != 'none':
        shirts_no_apron_and_dresses_torsos = filter_drops(girl_drops['torso'], wanted_styles=shirts_no_apron+dresses)
        return random_drop(shirts_no_apron_and_dresses_torsos) ##
    return random_drop(girl_drops['torso']) ##

def girl__get_legs_according_to_torso_and_jacket(torso, jacket):
    # onepiece torso styles: 24 25 26 27 28 29 30 31
    # dress torso styles: 32 33 34 35 36 37 38 39 40 41 42 43 44
    is_onepiece = torso in ('style24', 'style25', 'style26', 'style27', 'style28', 'style29', 'style30', 'style31')
    is_dress = torso in ('style32', 'style33', 'style34', 'style35', 'style36', 'style37', 'style38', 'style39', 'style40', 'style41', 'style42', 'style43', 'style44')
    if is_onepiece or is_dress:
        return 'none'
    # big jacket styles: 01 02 03 04 05
    is_bigjacket = jacket in ('style01', 'style02', 'style03', 'style04', 'style05')
    if is_bigjacket:
        # skirt legs styles: 12 13 14 15
        noskirt_legs = filter_drops(girl_drops['legs'], unwanted_styles=('style12', 'style13', 'style14', 'style15'))
        return random_drop(noskirt_legs) 
    return random_drop(girl_drops['legs']) 

def build_boy_char():
    char = {}
    char['rarity'] = 'TBD'
    char['gender'] = 'male'
    for slot in boy_drops:
        if slot == 'costume':
            char['costume'] = random_drop(boy_drops['costume'])
            if (char['costume']) != 'none':
                char['hat'] = 'none'
                char['hair'] = 'none'
                char['glasses'] = 'none' if char['costume'] != 'style01' else random_drop(boy_drops['glasses'])
                char['eyes'] = random_drop(boy_drops['eyes'])
                char['nose'] = 'style01'
                char['beard'] = 'none'
                char['bowtie'] = 'none'
                char['jacket'] = 'none'
                char['torso'] = 'none'
                char['legs'] = 'none'
                char['shoes'] = 'none'
                char['skin'] = random_drop(boy_drops['skin'])
                break
        elif slot == 'hair':
            char['hair'] = boy__get_hair_according_to_hat(char['hat'])
        elif slot == 'beard':
            char['beard'] = boy__get_beard_according_to_hair(char['hair'])
        elif slot == 'torso':
            char['torso'] = boy__get_torso_according_to_jacket(char['jacket'])
        elif slot == 'legs':
            char['legs'] = boy__get_legs_according_to_torso(char['torso'])
        else:
            char[slot] = random_drop(boy_drops[slot])
    char['points'] = get_char_points(char)
    char['rarity'] = get_char_rarity(char['points'], char['gender'])
    return char

def build_girl_char():
    char = {}
    char['rarity'] = 'TBD'
    char['gender'] = 'female'
    for slot in girl_drops:
        if slot == 'costume':
            char['costume'] = random_drop(girl_drops['costume'])
            if (char['costume']) != 'none':
                char['hat'] = 'none'
                char['hair'] = 'none' if char['costume'] != 'style01' else random_drop(filter_drops(girl_drops['hair'], wanted_styles=('style01',)))
                char['glasses'] = 'none' if char['costume'] != 'style01' else random_drop(girl_drops['glasses'])
                char['eyes'] = random_drop(girl_drops['eyes'])
                char['nose'] = 'style01'
                char['beard'] = 'none'
                char['bowtie'] = 'none'
                char['jacket'] = 'none'
                char['torso'] = 'none'
                char['legs'] = 'none'
                char['shoes'] = 'none'
                char['skin'] = random_drop(girl_drops['skin'])
                break
        elif slot == 'hair':
            char['hair'] = girl__get_hair_according_to_hat(char['hat'])
        elif slot == 'torso':
            char['torso'] = girl__get_torso_according_to_jacket(char['jacket'])
        elif slot == 'legs':
            char['legs'] = girl__get_legs_according_to_torso_and_jacket(char['torso'], char['jacket'])
        else:
            char[slot] = random_drop(girl_drops[slot])
    char['points'] = get_char_points(char)
    char['rarity'] = get_char_rarity(char['points'], char['gender'])
    return char

# returns visual signature of a costume character
def get_costume_signature(char):
    if char['costume'] == 'style01': # is astronaut
        signature = (char['costume'], char['eyes'], char['skin'], char['glasses'])
    else:
        signature = (char['costume'], char['eyes'], char['skin'])
    return signature

# resolves duplicity of costume characters visuals by checking their unique visual signatures
# changes in-place
def resolve_costume_twins(char_list, old_char_lists=[]):
    unique_signatures = []  
    for old_char_list in old_char_lists:
        for ind, char in enumerate(old_char_list):
            if char['costume'] != 'none':
                # gets visual signature
                signature = get_costume_signature(char)
                unique_signatures.append(signature)
    if (len(unique_signatures) != len(set(unique_signatures))): raise ValueError('old char lists contain twins')

    for ind, char in enumerate(char_list):
        if char['costume'] != 'none':
            # gets visual signature
            signature = get_costume_signature(char)
            # compares with those stored
            tries = 0
            while(signature in unique_signatures):
                print("id", ind, "duplicate costume found -", char['costume'], char['eyes'], char['skin'], "- rerolling...", tries)
                # reroll traits
                drops = boy_drops if char['gender'] == 'male' else girl_drops
                char['eyes'] = random_drop(drops['eyes'])
                char['skin'] = random_drop(drops['skin'])
                if char['costume'] == 'style01':
                    char['glasses'] = random_drop(drops['glasses'])
                signature = get_costume_signature(char)
                tries += 1
                # cant find unique combination, reroll costume
                if (tries > 99):
                    print("could not resolve visual signature conflict", char['costume'])
                    char['costume'] = random_drop(filter_drops(drops['costume'], unwanted_styles=('none', char['costume'])))
                    print("trying new costume", char['costume'])
                    signature = get_costume_signature(char)
                    tries = 0
            unique_signatures.append(signature)

# finds non-unique characters and replace them (~10% chance of happening in a 10_000 set)
# changes in-place
def resolve_twins(char_list, old_char_lists=[]):
    old_chars = []
    for old_char_list in old_char_lists:
        for ind, char in enumerate(old_char_list):
            if (char in old_chars): raise ValueError('old char lists contains twins')
            old_chars.append(char)
    
    tries = 0
    while(True):
        print("finding twins...")
        duplicate_ids = [i for i, char in enumerate(char_list) if (char in char_list[i+1:]) or (char in old_chars)]
        for ind in duplicate_ids:
            print("changing char", ind, char_list[ind])
            char_list[ind] = build_boy_char() if char_list[ind]['gender'] == 'male' else build_girl_char()
            print("new char", char_list[ind])
        if len(duplicate_ids) == 0: 
            print("no twins found")
            break
        tries += 1
        if (tries > 10):
            raise Exception("not converging")
            break

def get_char_points(char):
    drops_ref = lb_set_data.boy_drops_ref if char['gender'] == 'male' else lb_set_data.girl_drops_ref
    points = []
    for attr in char:
        if attr not in drops_ref: 
            continue
        if char[attr] == 'none': 
            # special rule: onepiece torso repeat rarity on legs
            if attr == 'legs' and char['torso'] != 'none':
                rarity = dict(drops_ref['torso'])[char['torso']]
                points.append(lb_set_data.drop_points[rarity])
            else:
                points.append(0)
            continue
        rarity = dict(drops_ref[attr])[char[attr]]
        points.append(lb_set_data.drop_points[rarity])
    return sum(points)

# different rarity requisites for male/female because of different item sets
def get_char_rarity(points, gender):
    if points >= 999: return 'iridescent'
    if gender == 'male':
        if points >= 49: return 'legendary'
        if points >= 44: return 'epic'
        if points >= 39: return 'rare'
        if points >= 34: return 'uncommon'
        return 'common'
    else:
        if points >= 45: return 'legendary'
        if points >= 41: return 'epic'
        if points >= 37: return 'rare'
        if points >= 32: return 'uncommon'
        return 'common'

def get_char_style_display(char, slot):
    display_attrs = lb_set_data.boy_styles_display if char['gender'] == 'male' else lb_set_data.girl_styles_display
    return display_attrs[slot][char[slot]]

# generate random unique lowercase strings
def get_random_names(n_names, n_letters, seed):
    random.seed(seed)
    names = []
    for _ in range(n_names):
        while True:
            name = ""
            for _ in range(n_letters):
                name += random.choice("abcdefghijklmnopqrstuvwxyz")
            if name not in names: break
        names.append(name)
    print("generated", n_names, "unique names:", len(names) == len(set(names)))
    return sorted(names)

def get_char_display(char):
    for attr in char:
        attr_value = char[attr].capitalize() if attr == 'rarity' or attr == 'gender' else get_char_style_display(char, attr)
        print(attr[:6] + ":\t", attr_value)
