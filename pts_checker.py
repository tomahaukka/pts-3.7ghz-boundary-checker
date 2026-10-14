import math
import argparse

class PTSBoundaryChecker:
    """
    Radiometric Analytics — Lightweight PTS Sweden 3.7 GHz Private 5G Boundary Compliance Engine.
    Calculates Worst-Case RSRP and FSPL at property boundaries (SWEREF 99 TM).
    """
    def __init__(self, freq_mhz=3750.0):
        self.freq_mhz = freq_mhz

    def calculate_fspl(self, distance_m):
        if distance_m < 0.1:
            distance_m = 0.1
        return 20 * math.log10(distance_m) + 20 * math.log10(self.freq_mhz) - 27.55

    def evaluate_boundary_point(self, tx_x, tx_y, boundary_x, boundary_y, eirp_dbm, wall_loss_db=0.0):
        distance = math.sqrt((tx_x - boundary_x)**2 + (tx_y - boundary_y)**2)
        fspl = self.calculate_fspl(distance)
        rsrp = eirp_dbm - fspl - wall_loss_db
        return {
            "distance_m": round(distance, 2),
            "fspl_db": round(fspl, 2),
            "rsrp_dbm": round(rsrp, 2)
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Radiometric PTS 3.7 GHz Boundary Compliance Engine")
    parser.add_argument("--dist", type=float, default=120.0, help="Distance to boundary in meters")
    parser.add_argument("--eirp", type=float, default=24.0, help="Transmitter EIRP in dBm")
    parser.add_argument("--wall", type=float, default=12.0, help="Outer wall attenuation in dB")
    args = parser.parse_args()

    checker = PTSBoundaryChecker(freq_mhz=3750.0)
    res = checker.evaluate_boundary_point(0, 0, args.dist, 0, eirp_dbm=args.eirp, wall_loss_db=args.wall)
    
    print("\n--- Radiometric Private 5G Compliance Evaluation ---")
    print(f"Target Distance:  {res['distance_m']} m")
    print(f"Calculated FSPL:  {res['fspl_db']} dB")
    print(f"Boundary RSRP:    {res['rsrp_dbm']} dBm")
    print("----------------------------------------------------\n")
