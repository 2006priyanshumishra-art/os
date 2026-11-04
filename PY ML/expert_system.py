print("Program is developed by",u"\u092A\u094D\u0930\u093F\u092F\u093E\u0902\u0936\u0941\u0020\u092E\u093F\u0936\u094D\u0930\u093E")
print("Program is checked by",u"\u0935\u0948\u0936\u093E\u0932\u0940\u0020\u0907\u0902\u0917\u0933\u0947 / \u0936\u094d\u0935\u0947\u0924\u093e \u0935\u093e\u0928\u0916\u0947\u0921\u093c\u0947")
print("Date of performance - 2 Sep 2026")

# ==========================================
# CELL 1: KNOWLEDGE BASE DEFINITIONS (AND/OR PERMUTATIONS)
# ==========================================

KNOWLEDGE_BASES = {
    "1": {
        "name": "Vehicle Fault Diagnosis",
        "facts": [
            "engine_not_starting", "battery_low", "headlights_dim", "fuel_low",
            "engine_overheating", "coolant_low", "engine_noise", "oil_low",
            "warning_light_on", "starter_clicking", "vehicle_old"
        ],
        "rules": [
            # IF battery_low AND (headlights_dim OR starter_clicking)
            (("AND", "battery_low", ("OR", "headlights_dim", "starter_clicking")), "electrical_system_weak"),
            
            # IF electrical_system_weak AND engine_not_starting
            (("AND", "electrical_system_weak", "engine_not_starting"), "starting_system_fault"),
            
            # IF starting_system_fault AND vehicle_old
            (("AND", "starting_system_fault", "vehicle_old"), "battery_replacement_required"),
            
            # IF (fuel_low OR battery_low) AND engine_not_starting
            (("AND", ("OR", "fuel_low", "battery_low"), "engine_not_starting"), "fuel_or_ignition_check"),
            
            # IF engine_overheating AND (coolant_low OR oil_low)
            (("AND", "engine_overheating", ("OR", "coolant_low", "oil_low")), "cooling_or_lube_fault")
        ],
        "goals": ["electrical_system_weak", "starting_system_fault", "battery_replacement_required", "fuel_or_ignition_check", "cooling_or_lube_fault"]
    },
    "2": {
        "name": "Agriculture / Crop Advisory",
        "facts": [
            "soil_dry", "temperature_high", "humidity_low", "leaves_yellow", "rainfall_low",
            "leaf_edges_brown", "irrigation_irregular", "fertilizer_recently_applied"
        ],
        "rules": [
            # IF soil_dry AND (temperature_high OR humidity_low)
            (("AND", "soil_dry", ("OR", "temperature_high", "humidity_low")), "severe_water_stress"),
            
            # IF (rainfall_low AND irrigation_irregular) OR soil_dry
            (("OR", ("AND", "rainfall_low", "irrigation_irregular"), "soil_dry"), "irrigation_deficiency"),
            
            # IF severe_water_stress AND irrigation_deficiency
            (("AND", "severe_water_stress", "irrigation_deficiency"), "urgent_irrigation_required"),
            
            # IF leaves_yellow AND (leaf_edges_brown OR fertilizer_recently_applied)
            (("AND", "leaves_yellow", ("OR", "leaf_edges_brown", "fertilizer_recently_applied")), "nutrient_check_required")
        ],
        "goals": ["severe_water_stress", "irrigation_deficiency", "urgent_irrigation_required", "nutrient_check_required"]
    },
    "3": {
        "name": "Network Troubleshooting",
        "facts": [
            "internet_not_working", "router_off", "wifi_not_visible", "cable_disconnected",
            "power_fluctuation", "multiple_devices_affected", "dns_failure"
        ],
        "rules": [
            # IF router_off OR (power_fluctuation AND wifi_not_visible)
            (("OR", "router_off", ("AND", "power_fluctuation", "wifi_not_visible")), "router_power_issue"),
            
            # IF internet_not_working AND (cable_disconnected OR router_power_issue)
            (("AND", "internet_not_working", ("OR", "cable_disconnected", "router_power_issue")), "network_down"),
            
            # IF network_down AND multiple_devices_affected AND dns_failure
            (("AND", "network_down", "multiple_devices_affected", "dns_failure"), "isp_failure_suspected")
        ],
        "goals": ["router_power_issue", "network_down", "isp_failure_suspected"]
    },
    "4": {
        "name": "Cybersecurity Alert System",
        "facts": [
            "multiple_failed_logins", "unknown_device", "unusual_location", "password_changed",
            "admin_account", "large_data_transfer", "antivirus_disabled"
        ],
        "rules": [
            # IF unknown_device AND (multiple_failed_logins OR unusual_location)
            (("AND", "unknown_device", ("OR", "multiple_failed_logins", "unusual_location")), "suspicious_login"),
            
            # IF suspicious_login AND (password_changed OR admin_account)
            (("AND", "suspicious_login", ("OR", "password_changed", "admin_account")), "high_risk_account_compromise"),
            
            # IF (large_data_transfer AND antivirus_disabled) OR high_risk_account_compromise
            (("OR", ("AND", "large_data_transfer", "antivirus_disabled"), "high_risk_account_compromise"), "critical_security_incident")
        ],
        "goals": ["suspicious_login", "high_risk_account_compromise", "critical_security_incident"]
    }
}
print("Advanced AND/OR Knowledge Bases Loaded!")

# ==========================================
# CELL 2: INFERENCE ENGINES
# ==========================================

def format_rule(condition):
    """Helper to print nested tuple rules nicely as Strings"""
    if isinstance(condition, str):
        return condition
    op = condition[0]
    args = [format_rule(arg) for arg in condition[1:]]
    if op == "AND": return "(" + " AND ".join(args) + ")"
    if op == "OR":  return "(" + " OR ".join(args) + ")"

def evaluate_forward(condition, facts):
    """Recursively checks if a logic condition is met based on current facts"""
    if isinstance(condition, str):
        return condition in facts
    
    op = condition[0]
    if op == "AND":
        return all(evaluate_forward(arg, facts) for arg in condition[1:])
    elif op == "OR":
        return any(evaluate_forward(arg, facts) for arg in condition[1:])
    return False

def forward_chaining(known_facts, rules, target_goal):
    inferred_facts = set(known_facts)
    new_fact_added = True

    print("\n--- Forward Chaining Execution ---")
    while new_fact_added:
        new_fact_added = False
        for condition, conclusion in rules:
            if conclusion not in inferred_facts:
                # Use our recursive evaluator
                if evaluate_forward(condition, inferred_facts):
                    inferred_facts.add(conclusion)
                    rule_str = f"IF {format_rule(condition)} THEN {conclusion}"
                    print(f"-> Inferred: {conclusion}")
                    print(f"   [Rule Matched]: {rule_str}")
                    new_fact_added = True
                    
                    if conclusion == target_goal:
                        print(f"\n=> TARGET GOAL '{target_goal}' REACHED!")
                        return True

    print(f"\n=> Target Goal '{target_goal}' could NOT be inferred.")
    return False


def backward_chaining(known_facts, rules, target_goal):
    print("\n--- Backward Chaining Execution ---")
    
    def evaluate_backward(condition, visited, indent="  "):
        """Recursively tries to prove conditions working backwards"""
        if isinstance(condition, str):
            return verify(condition, visited, indent)
            
        op = condition[0]
        if op == "AND":
            print(f"{indent}Checking AND condition...")
            for arg in condition[1:]:
                if not evaluate_backward(arg, visited.copy(), indent + "  "):
                    return False
            return True
            
        elif op == "OR":
            print(f"{indent}Checking OR condition...")
            for arg in condition[1:]:
                if evaluate_backward(arg, visited.copy(), indent + "  "):
                    return True
            return False

    def verify(goal, visited, indent="  "):
        if goal in known_facts:
            print(f"{indent}[Known Fact] '{goal}' is TRUE.")
            return True
        if goal in visited:
            return False
            
        visited.add(goal)
        print(f"{indent}[Investigating Goal] {goal}")
        
        for condition, conclusion in rules:
            if conclusion == goal:
                rule_str = f"IF {format_rule(condition)} THEN {conclusion}"
                print(f"{indent}-> Found Rule: {rule_str}")
                
                if evaluate_backward(condition, visited.copy(), indent + "  "):
                    print(f"{indent}=> PROVED: {goal}")
                    return True
                    
        return False

    result = verify(target_goal, set())
    if result:
        print(f"\n=> Target Goal '{target_goal}' was PROVEN TRUE.")
    else:
        print(f"\n=> Target Goal '{target_goal}' could NOT be proven.")
    return result

print("Advanced Inference Engines Loaded!")

# ==========================================
# CELL 3: INTERACTIVE UI (Updated with Engine Loop)
# ==========================================
from IPython.display import clear_output

def display_facts_and_rules(kb):
    print(f"\n=== FACTS for {kb['name']} ===")
    for i, fact in enumerate(kb['facts'], 1):
        print(f"  {i}. {fact}")
        
    print(f"\n=== LOGICAL RULES for {kb['name']} ===")
    for i, (condition, conclusion) in enumerate(kb['rules'], 1):
        print(f"  Rule {i}: IF {format_rule(condition)} THEN {conclusion}")
    input("\nPress Enter to continue...")

def find_inferences(kb):
    print("\n--- Define Current State ---")
    for i, fact in enumerate(kb['facts'], 1):
        print(f"[{i}] {fact}")
        
    fact_inputs = input("\nEnter numbers of known TRUE facts (comma-separated): ").split(",")
    known_facts = set()
    for fi in fact_inputs:
        if fi.strip().isdigit():
            idx = int(fi.strip()) - 1
            if 0 <= idx < len(kb['facts']):
                known_facts.add(kb['facts'][idx])
    
    print(f"\nActive Facts: {known_facts}")

    print("\n--- Select Target Goal ---")
    for i, goal in enumerate(kb['goals'], 1):
        print(f"[{i}] {goal}")
        
    try:
        goal_idx = int(input("\nEnter goal number: ")) - 1
        target_goal = kb['goals'][goal_idx]
    except (ValueError, IndexError):
        print("Invalid goal selection.")
        return

    # NEW: Loop to allow multiple engine runs on the same facts/goal
    while True:
        print(f"\n" + "-"*40)
        print(f" Target Goal: {target_goal}")
        print("-"*40)
        print("Choose Action:")
        print("  1. Run Forward Chaining")
        print("  2. Run Backward Chaining")
        print("  3. Go Back (Change Facts/Goal or Exit)")
        
        engine_choice = input("> ")

        if engine_choice == "1":
            forward_chaining(known_facts, kb['rules'], target_goal)
            input("\n[Press Enter to choose engine again...]")
        elif engine_choice == "2":
            backward_chaining(known_facts, kb['rules'], target_goal)
            input("\n[Press Enter to choose engine again...]")
        elif engine_choice == "3":
            print("Returning to menu...")
            break
        else:
            print("Invalid selection. Please choose 1, 2, or 3.")

def start_expert_system():
    while True:
        clear_output(wait=True)
        print("#"*40)
        print("EXPERT SYSTEM")
        print("#"*40)
        print("1. Vehicle Fault Diagnosis")
        print("2. Agriculture / Crop Advisory")
        print("3. Network Troubleshooting")
        print("4. Cybersecurity Alert System")
        print("5. Exit")
        print("#"*40)
        
        main_choice = input("Enter your choice (1-5): ")
        
        if main_choice == '5': 
            print("Exiting Expert System.")
            break
            
        if main_choice in KNOWLEDGE_BASES:
            kb = KNOWLEDGE_BASES[main_choice]
            while True:
                clear_output(wait=True)
                print(f"="*40)
                print(f" {kb['name'].upper()}")
                print("="*40)
                print("1. Display Facts and Logic Rules")
                print("2. Find Inferences")
                print("3. Return to Main Menu")
                
                sub_choice = input("> ")
                if sub_choice == '1': 
                    display_facts_and_rules(kb)
                elif sub_choice == '2': 
                    find_inferences(kb)
                elif sub_choice == '3': 
                    break

# Run the program
start_expert_system()
