#type: ignore
import model
import matplotlib.pyplot as plt

if __name__ == "__main__":
    pixel_size = 75
    electrons_num = 2200
    hit_pos = 50
    fig_size = 40

    px_model = model.PixelChargeSharingModel1D(pixel_size)
    px_model.hit(hit_pos, electrons_num)
    calc_hit_ideal = px_model.calc_hit_1D_ideal()

    print(f"{hit_pos=} μm")
    print(f"{calc_hit_ideal=} μm")
    print(f"{px_model.sigma=} μm")

    ax = plt.axes()
    title = f"1D charge distribution.\n Real hit at {hit_pos:2.3f} μm. Calculated hit at {calc_hit_ideal:2.3f}μm"
    px_model.set_plt_axis_distribution(ax, title, fig_size)
    plt.show()
