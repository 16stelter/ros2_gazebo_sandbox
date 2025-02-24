#include <gz/sim/System.hh>
#include <gz/sim/Model.hh>
#include <gz/sim/components.hh>
#include "gz/sim/components/Link.hh"
#include "gz/sim/Link.hh"
#include <gz/plugin/Register.hh>
#include <gz/transport/Node.hh>
#include <gz/msgs/twist.pb.h>
#include "gz/sim/components/LinearVelocity.hh"
#include "gz/sim/components/AngularVelocity.hh"
#include "gz/sim/Util.hh"

using namespace gz;
using namespace sim;
using namespace systems;

namespace gz_plugins
{
class FakeFlightController
  : public System,
    public ISystemConfigure,
    public ISystemUpdate
{
  Model model_{kNullEntity};
  double force_constant_;
  bool configured_{false};
  Link base_link_;
  EntityComponentManager *ecm_ = nullptr;
  gz::transport::Node node_;
  msgs::Twist last_msg_;
  std::string topic_;

public:
  void Configure(
    const Entity & entity, 
    const std::shared_ptr<const sdf::Element> & sdf,
    EntityComponentManager & ecm,
    EventManager & /*eventMgr*/) override
  {
    model_ = Model(entity);

    if (!model_.Valid(ecm)) {
      gzerr  << "FakeFlightController plugin should be attached to a model "
             << "entity. Failed to initialize." << std::endl;
      return;
    }

    force_constant_ = 1.0;
    if (!sdf->HasElement("forceConstant")) {
      gzwarn << "No forceConstant element present. Setting forceConstant = 1.0" <<
        std::endl;
    }
    else
    {
      force_constant_ = sdf->Get<double>("forceConstant");
    }

    if (!sdf->HasElement("topic")) {
      gzerr << "No topic specified. Aborting." <<
        std::endl;
      return;
    }
    topic_ = sdf->Get<std::string>("topic");
    

    enableComponent<components::WorldAngularVelocity>(ecm,
          base_link_.Entity());
    enableComponent<components::WorldLinearVelocity>(ecm,
          base_link_.Entity());

    ecm_ = &ecm;
    configured_ = true;

    node_.Subscribe(topic_, &FakeFlightController::OnMessage, this);

    base_link_ = Link(model_.LinkByName(ecm, "base_link"));
  }

  void Update(
    const UpdateInfo & info,
    EntityComponentManager & ecm) override
  {
    if (!configured_ || info.paused) {return;}

    if (last_msg_.has_linear() && last_msg_.has_angular()) {
      math::Vector3 force(last_msg_.linear().x() * force_constant_,
                          last_msg_.linear().y() * force_constant_,
                          last_msg_.linear().z() * force_constant_);

      math::Vector3 torque(last_msg_.angular().x() * force_constant_,
                           last_msg_.angular().y() * force_constant_,
                           last_msg_.angular().z() * force_constant_);
      
      base_link_.AddWorldWrench(*ecm_, force, torque);
    }
  }

private:
  void OnMessage(const msgs::Twist &msg)
  {
    last_msg_ = msg;

    gzdbg << "Received message: force(" 
          << msg.linear().x() << ", "
          << msg.linear().y() << ", "
          << msg.linear().z() << ") torque("
          << msg.angular().x() << ", "
          << msg.angular().y() << ", "
          << msg.angular().z() << ")" << std::endl;
}
};

}  // namespace gz_plugins

GZ_ADD_PLUGIN(
  gz_plugins::FakeFlightController,
  System,
  gz_plugins::FakeFlightController::ISystemConfigure,
  gz_plugins::FakeFlightController::ISystemUpdate)
