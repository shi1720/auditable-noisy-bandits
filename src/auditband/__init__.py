"""Cost-sensitive learning with a shared auditable binary channel."""
from .model import Environment, paired_instance, joint_law, kl, compatible_interval, robust_winners, ambiguity_lp
from .policy import ScaleUCB
