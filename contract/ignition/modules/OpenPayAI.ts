import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

export default buildModule("OpenPayAIModule", (m) => {
  const deployer = m.getAccount(0);
  const openPayAI = m.contract("OpenPayAI", [
    deployer,
    "0x6c3ea9036406852006290770BEdFcAbA0e23A0e8",
  ]);

  return { openPayAI };
});
