import bornagain as ba
from bornagain import deg, nm


def getSample():
    # Defining Materials
    material_2 = ba.HomogeneousMaterial("Si", 7.6e-06, 1.7e-07)
    material_1 = ba.HomogeneousMaterial("Air", 0.0, 0.0)

    # Defining Layers
    layer_1 = ba.Layer(material_1)
    layer_2 = ba.Layer(material_2)

    # Defining Form Factors
    formFactor_1 = ba.FormFactorCylinder(5.0 * nm, 5.0 * nm)

    # Defining Particles
    particle_1 = ba.Particle(material_2, formFactor_1)

    # Defining particles with parameter following a distribution
    distr_1 = ba.DistributionGaussian(5.0, 1.0)
    par_distr_1 = ba.ParameterDistribution("/Particle/Cylinder/Radius", distr_1, 10, 2.0)
    par_distr_1.linkParameter("/Particle/Cylinder/Height")
    particleDistribution_1 = ba.ParticleDistribution(particle_1, par_distr_1)

    # Defining Particle Layouts and adding Particles
    layout_1 = ba.ParticleLayout()
    layout_1.addParticle(particleDistribution_1, 1.0)
    layout_1.setTotalParticleSurfaceDensity(1)

    # Adding layouts to layers
    layer_1.addLayout(layout_1)

    # Defining Multilayers
    multiLayer_1 = ba.MultiLayer()
    multiLayer_1.addLayer(layer_1)
    multiLayer_1.addLayer(layer_2)
    return multiLayer_1


def getSimulation():
    simulation = ba.GISASSimulation()
    simulation.setDetectorParameters(200, -2.0 * deg, 2.0 * deg, 200, 0.0 * deg, 2.0 * deg)

    simulation.setBeamParameters(0.154 * nm, 0.2 * deg, 0.0 * deg)
    simulation.setBeamIntensity(1.0e+08)
    distribution_1 = ba.DistributionGaussian(0.00349065850399, 0.00174532925199)
    simulation.addParameterDistribution("*/Beam/InclinationAngle", distribution_1, 10, 2.0)
    return simulation


def plot(intensities):
    import matplotlib.colors
    from matplotlib import pyplot as plt
    im = plt.imshow(intensities.getArray(), norm=matplotlib.colors.LogNorm(1, intensities.getMaximum()),
                    extent=[-2.0, 2.0, 0.0, 2.0], aspect='auto')
    plt.colorbar(im)
    plt.show()


def simulate():
    # Run Simulation
    sample = getSample()
    simulation = getSimulation()
    simulation.setSample(sample)
    simulation.runSimulation()
    return simulation.getIntensityData()


if __name__ == '__main__':
    ba.simulateThenPlotOrSave(simulate, plot)