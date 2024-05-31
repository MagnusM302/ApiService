# building_microservices/app_user/models/building_report.py

class BuildingReport:
    def __init__(self, address, inspection_date, inspector_name, client_name, client_contact, building_type, construction_year, renovation_history, building_materials, roof_type, foundation_type, total_area, buildings, wall_conditions, roof_conditions, floor_conditions, windows_doors_conditions, moisture_mold, electrical_system, plumbing_system, heating_system, asbestos, radon, lead_paint, exterior_walls, yard_landscaping, driveways_walkways, interior_rooms, attic_conditions, basement_conditions, insulation):
        self.address = address
        self.inspection_date = inspection_date
        self.inspector_name = inspector_name
        self.client_name = client_name
        self.client_contact = client_contact
        self.building_type = building_type
        self.construction_year = construction_year
        self.renovation_history = renovation_history
        self.building_materials = building_materials
        self.roof_type = roof_type
        self.foundation_type = foundation_type
        self.total_area = total_area
        self.buildings = buildings
        self.wall_conditions = wall_conditions
        self.roof_conditions = roof_conditions
        self.floor_conditions = floor_conditions
        self.windows_doors_conditions = windows_doors_conditions
        self.moisture_mold = moisture_mold
        self.electrical_system = electrical_system
        self.plumbing_system = plumbing_system
        self.heating_system = heating_system
        self.asbestos = asbestos
        self.radon = radon
        self.lead_paint = lead_paint
        self.exterior_walls = exterior_walls
        self.yard_landscaping = yard_landscaping
        self.driveways_walkways = driveways_walkways
        self.interior_rooms = interior_rooms
        self.attic_conditions = attic_conditions
        self.basement_conditions = basement_conditions
        self.insulation = insulation

    def to_dict(self):
        return self.__dict__
