import { network, artifacts } from "hardhat";

const { viem } = await network.connect({
  network: "localhost",
  chainType: "op",
});

const [walletClient] = await viem.getWalletClients();
const artifact = await artifacts.readArtifact("MockPYUSD");
const PYUSD_ADDRESS = "0x6c3ea9036406852006290770BEdFcAbA0e23A0e8";

await walletClient.request({
  method: "hardhat_setCode",
  params: [PYUSD_ADDRESS, artifact.deployedBytecode],
});
console.log(`MockPYUSD bytecode injected at ${PYUSD_ADDRESS}`);

const pyusd = await viem.getContractAt("MockPYUSD", PYUSD_ADDRESS, {
  client: walletClient,
});

const recipient = "0x8626f6940e2eb28930efb4cef49b2d1f2c9c1199";
const decimals = 6n;
const amount = 100n * 10n ** decimals;
await pyusd.write.mint([recipient, amount]);

console.log(`Minted 100 PYUSD to ${recipient}`);
