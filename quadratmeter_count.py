from archicad import ACConnection

conn = ACConnection.connect()
assert conn
acc = conn.commands
act = conn.types
acu = conn.utilities

# 1. Get selected elements
selected = acc.GetSelectedElements(onlySupportedTypes=True)

if not selected:
    print("No elements selected!")
else:
    # 2. Filter to only Zone elements
    types_of = acc.GetTypesOfElements(selected)
    
    zone_ids = [
        el for el, t in zip(selected, types_of)
        if t.typeOfElement is not None and t.typeOfElement.elementType == 'Zone'
    ]

    if not zone_ids:
        print("No Zone elements in selection!")
    else:
        print(f"Found {len(zone_ids)} zone(s).")

        # 3. Get the calculated area property
        prop_id = acu.GetBuiltInPropertyId('Zone_CalculatedArea')
        results = acc.GetPropertyValuesOfElements(zone_ids, [prop_id])

        # 4. Sum the areas
        total = 0.0
        count = 0
        for res in results:
            for pv in res.propertyValues:
                if pv.propertyValue.status == 'normal':
                    try:
                        total += float(pv.propertyValue.value)
                        count += 1
                    except (TypeError, ValueError):
                        pass

        print(f"Summed {count} zone area(s)")
        print(f"Total: {total:.2f} m²")