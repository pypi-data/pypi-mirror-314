import pandas as pnd
import cobra


def check_gpr(logger, rid, row, kr_ids, idcollection_dict, addtype='R'): 
    
    itemtype = 'Reaction' if addtype=='R' else 'Transporter'
    
    # check presence of the GPR
    if pnd.isna(row['gpr_manual']): 
        logger.error(f"{itemtype} '{rid}' has missing GPR: '{row['gpr_manual']}'.")
        return 1
    
    # get ko_ids in this reaction:
    ko_ids_parsed = row['gpr_manual'].strip()
    ko_ids_parsed = ko_ids_parsed.replace(' and ', ',')
    ko_ids_parsed = ko_ids_parsed.replace(' or ', ',')
    ko_ids_parsed = ko_ids_parsed.replace('(', '')
    ko_ids_parsed = ko_ids_parsed.replace(')', '')
    ko_ids_parsed = ko_ids_parsed.split(',')
    
    
    # collect all the ko_ids for this reaction:
    if addtype=='R':
        ko_for_rid = set()   
        for kr_id in kr_ids:
            if kr_id == 'RXXXXX': 
                continue
            ko_for_rid = ko_for_rid.union(idcollection_dict['kr_to_ko'][kr_id])
            
    
    # check if these ko_ids exist:
    for ko_id in ko_ids_parsed:
        ko_id = ko_id.strip() 
        if ko_id not in idcollection_dict['ko'] and ko_id != 'spontaneous':
            logger.error(f"{itemtype} '{rid}' has an invalid KEGG Ortholog: '{ko_id}'.")
            return 1
        
        
        # check if these ko_ids are really assigned to this reaction:
        if addtype=='R':
            if ko_id not in ko_for_rid and ko_id != 'spontaneous':
                logger.debug(f"Ortholog '{ko_id}' should not be linked to reaction '{rid}' (available for {kr_ids}: {ko_for_rid}).")
            
    
    # check if some ko_ids are missing from this reaction:
    if addtype=='R':
        missing_ko_ids = ko_for_rid - (set(ko_ids_parsed) - set(['spontaneous']))
        if len(missing_ko_ids) > 0:
            logger.debug(f"Orthologs {missing_ko_ids} are missing from reaction '{rid}' ({kr_ids}).")
            #return 1
            
            
    return 0
                



def add_reaction(logger, model, rid, row, kr_ids, addtype='R'):
    
    
    itemtype = 'Reaction' if addtype=='R' else 'Transporter'
    
    
    r = cobra.Reaction(rid)
    model.add_reactions([r])
    r = model.reactions.get_by_id(rid)
    r.build_reaction_from_string(row['rstring'])
    r.name = row['name'].strip()
    r.bounds = (0, 1000) if ' --> ' in row['rstring'] else (-1000,  1000)
    r.gene_reaction_rule = row['gpr_manual'].strip()
    r.update_genes_from_gpr()
    for m in r.metabolites:
        if m.formula == None or m.charge == None:
            logger.error(f"Metabolite '{m.id}' appears in '{r.id}' but was not previously defined.")
            return 1
        
        
    if addtype == 'R':
        # add kr annotations to model
        r.annotation['kegg.reaction'] = kr_ids
        
        
    # check if unbalanced
    if r.check_mass_balance() != {}: 
        logger.error(f"{itemtype} '{r.id}' is unbalanced: {r.check_mass_balance()}.")
        return 1    
    
    
    return 0



def check_rstring_arrow(logger, row, addtype='R'):
    
    itemtype = 'Reaction' if addtype=='R' else 'Transporter'
    
    
    if pnd.isna(row['rstring']): 
        logger.error(f"{itemtype} '{rid}' has no definition (rstring).")
        return 1
    if ' --> ' not in row['rstring'] and ' <=> ' not in row['rstring']:
        logger.error(f"{itemtype} '{rid}' has invalid arrow: '{row['rstring']}'.")
        return 1
        
        
    return 0



def check_author(logger, mrid, row, db, addtype='R'): 
    
    
    if addtype=='M':
        itemtype = 'Metabolite'
    elif  addtype=='R' :
        itemtype = 'Reaction'
    else: itemtype = 'Transporter'
    
    
    if pnd.isna(row['author']): 
        logger.error(f"{itemtype} '{mrid}' has no author.")
        return 1
    for author in row['author'].split(';'):
        author = author.strip()
        if author not in db['authors']['username'].to_list(): 
            logger.error(f"{itemtype} '{mrid}' has invalid author: '{author}'.")
            return 1
    
    
    return 0
    