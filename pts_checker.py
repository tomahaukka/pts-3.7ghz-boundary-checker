import math

class PTSBoundaryChecker:
    """
    Lightweight PTS Sweden 3.7 GHz Private 5G Boundary Compliance Engine.
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
    checker = PTSBoundaryChecker(freq_mhz=3750.0)
    # Example calculation: Transmitter at (X=150000, Y=6400000), Boundary at 120m distance
    res = checker.evaluate_boundary_point(150000, 6400000, 150120, 6400000, eirp_dbm=24.0, wall_loss_db=12.0)
    print(f"PTS Compliance Test Result: {res}")
