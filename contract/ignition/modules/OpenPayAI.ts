import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

export default buildModule("OpenPayAIModule", (m) => {
  const deployer = m.getAccount(0);
  const openPayAI = m.contract("OpenPayAI", [deployer]);

  return { openPayAI };
});
